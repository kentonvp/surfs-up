import math
from pprint import PrettyPrinter
import threading
import time
import traceback
import pandas as pd
from surfsup.maps import Location, distance_miles

from surfsup.surfline.api import SurflineAPI
from surfsup.dto.forecast_dto import ConditionRecord, WindRecord, \
        SwellRecord, WaveHeightRecord, TideRecord, TideCollectionRecord, \
        WeatherRecord, ForecastRecord


def or_none(name, func, json_arg, err_verbose:bool = False):
    try:
        return func(json_arg)
    except Exception:
        if err_verbose:
            print(f'ERR: Failure to parse {name}')
            pp = PrettyPrinter(indent=2)
            pp.pprint(json_arg)
    return None


def parse_conditions(fcst_json):
    cond = fcst_json['conditions']
    return ConditionRecord(
            cond['human'],
            cond['value'],
            cond['expired']
            )


def parse_wind(fcst_json):
    wind = fcst_json['wind']
    return WindRecord(
            wind['speed'],
            wind['direction']
            )


def parse_swell(swell_json):
    return SwellRecord(
            swell_json['height'],
            swell_json['period'],
            swell_json['direction'],
            swell_json['directionMin']
            )


def parse_swells(fcst_json):
    swells = []
    sorted_swells = sorted(fcst_json['swells'], key=lambda x: x['index'])
    for swell in sorted_swells:
        swells.append(parse_swell(swell))

    return swells


def parse_wave_height(fcst_json):
    wave = fcst_json['waveHeight']
    return WaveHeightRecord(
            wave['human'],
            wave['min'],
            wave['max'],
            wave['occasional'],
            wave['humanRelation'],
            wave['plus']
            )


def parse_tide(tide_json):
    return TideRecord(
            tide_json['type'],
            tide_json['height'],
            tide_json['timestamp'],
            tide_json['utcOffset']
            )


def parse_tides_collection(fcst_json):
    tides = fcst_json['tide']
    return TideCollectionRecord(
            parse_tide(tides['previous']),
            parse_tide(tides['current']),
            parse_tide(tides['next'])
            )


def parse_weather(fcst_json):
    return WeatherRecord(
            fcst_json['waterTemp']['min'],
            fcst_json['waterTemp']['max'],
            fcst_json['weather']['temperature'],
            fcst_json['weather']['condition']
            )


def parse_forecast_info(forecast_info):
    return ForecastRecord(
            forecast_info['note'],
            or_none('conditions', parse_conditions, forecast_info, False),
            or_none('wind', parse_wind, forecast_info, False),
            or_none('swells', parse_swells, forecast_info, False),
            or_none('wave_height', parse_wave_height, forecast_info, False),
            or_none('tides', parse_tides_collection, forecast_info, False),
            or_none('weather', parse_weather, forecast_info, False)
            )

class ForecastFetcher:
    surfline: SurflineAPI
    lck: threading.Lock
    err_tracker: list[str]
    nthreads: int
    pp: PrettyPrinter = PrettyPrinter(indent=2)
    verbose: int

    def __init__(self, db_path: str, nthreads: int = 16, verbose: int = 0):
        self.surfline = SurflineAPI(db_path)
        self.lck = threading.Lock()
        self.nthreads = nthreads
        self.err_tracker = []
        self.verbose = verbose

    def retrieve_forecast(self, names, spot_forecast):
        cnt: int = 0
        for spot_name in names:
            spot_data = {}
            try:
                spot_data = self.surfline.spot_check(spot_name)
            except Exception as exc:
                print(f'ERROR {exc}') if self.verbose > 0 else None

            try:
                if not spot_data:
                    print('Spot data is empty') if self.verbose > 0 else None
                    continue

                forecast_info = spot_data['forecast']
                fcst = parse_forecast_info(forecast_info)
                with self.lck:
                    spot_forecast[spot_name] = fcst
                cnt += 1
            except Exception as exc:
                self.err_tracker.append(spot_name)
                track = traceback.format_exc(limit=1)
                print(f'[[Thread-{threading.currentThread().name}]] ERROR: {spot_name}:\n' + track + \
                    f'----------Current count: {cnt}') if self.verbose > 0 else None

        self.pp.pprint(spot_forecast) if self.verbose > 0 else None
        return spot_forecast

    def by_loc(self, loc: Location, max_radius: int):
        # deep copy ? do we need to do this? maybe to do inplace sort?
        df = self.surfline.database.table.copy()

        distance_fn = lambda row: distance_miles(loc, Location(row['latitude'], row['longitude']))

        stime = time.time()
        df['distance'] = df.apply(distance_fn, axis=1)
        df.sort_values(by='distance', inplace=True)
        print(f'Calculating distance from user and sorting took {time.time() - stime}')
        print(df.head())

        stime = time.time()
        in_range = df.apply(lambda row: row['distance'] <= max_radius, axis=1)
        df = df[in_range] if len(df[in_range]) > 0 else df.head()
        print(f"Filtering took {time.time() - stime}: found {len(list(df['name']))}")

        stime = time.time()
        results_dict = self.runner(list(df['name']))
        print(f'Retrieval took {time.time() - stime}: found {len(df)}')

        return results_dict, dict(zip(df['name'],df['distance']))

    def _average(self, iter):
        n = len(iter)
        return sum(iter)/n

    def top_sorted(self, forecasts: dict, max_height:int, n: int = 5):
        df = self.to_df(forecasts)
        def conditions_score(c):
            conditions_order = [None, 'VERY_POOR', 'FLAT', 'POOR', 'POOR_TO_FAIR', 'FAIR', 'FAIR_TO_GOOD', 'GOOD', 'GOOD_TO_EPIC', 'EPIC']
            return conditions_order.index(c) / 7

        def height_score(s, max_height: int = 8):
            if s > max_height + 2:
                s = 0
            return s/max_height

        def wind_score(speed, dir, swell_dir):
            # is offshore: check against swell direction
            opp_wind = (dir + 180) % 360

            wind_score = -abs(opp_wind - swell_dir) / 180
            if abs(wind_score) <= 0.5:
                return wind_score + (self._inside(speed, 25))/25
            else:
                return wind_score - (self._inside(speed, 25))/25

        def total_score(row):
            return self._average(
                [
                    conditions_score(row['conditions']),
                    height_score(row['wave_min'], max_height),
                    height_score(row['wave_max'] if row['wave_occ'] == None else max(row['wave_max'], row['wave_occ']), max_height),
                    wind_score(row['wind_speed'], row['wind_dir'], row['swell_dir'])
                ]
            )

        df['sortable'] = df.apply(total_score, axis=1)
        df.sort_values(by='sortable', ascending=False, inplace=True)
        return df.head(n)

    def _inside(self, idx: int, length: int):
        return min(max(0, idx), length)

    def _recursive_dict_len(self, pool: dict):
        total_cnt: int = 0
        for k in pool.keys():
            res = pool[k]
            total_cnt += len(res)
        return total_cnt

    def to_df(self, forecast_infos: dict[str, ForecastRecord]):
        data = []
        for (spot_name, fcst) in forecast_infos.items():
            data.append(
                [spot_name,
                fcst.conditions.value,
                fcst.wind.speed,
                fcst.wind.direction,
                fcst.wave_height.min,
                fcst.wave_height.max,
                fcst.wave_height.occasional,
                fcst.swells[0].direction])

        return pd.DataFrame(data, columns=['name','conditions','wind_speed','wind_dir','wave_min','wave_max','wave_occ','swell_dir'])

    def to_csv(self, filename: str, forecast_infos: dict[str, ForecastRecord]) -> None:
        with open(filename, "a+") as fname:
            fname.write(','.join([
                'name',
                'conditions',
                'wind_speed',
                'wind_dir',
                'wave_min',
                'wave_max',
                'wave_occ',
                'swell_ht',
                'swell_per',
                'swell_dir',
                'ptide_ht',
                'ptide_ts',
                'ctide_ht',
                'ctide_ts',
                'ntide_ht',
                'ntide_ts',
                'temp',
                'water_low',
                'water_high'
            ]) + '\n')
            for (spot_name, fcst) in forecast_infos.items():
                name = spot_name
                fname.write(','.join([name, fcst.as_csv()]) + '\n')

        return None

    def runner(self, names: list[str] = []):
        print(f'[ STARTING RUNNER - ForecastRetrieval {self.nthreads}-threads ]############') if self.verbose > 0 else None
        if len(names) == 0:
            names = self.surfline.get_spot_names()
        else:
            assert self.surfline.validate_names(names)

        # Pull forecast for all spots and format to ForecastRecord
        res_pool = dict()
        thread_pool = list[threading.Thread]()
        if len(names) < self.nthreads:
            # if less than the number of threads just do on a single thread
            res_pool[0] = dict()
            self.retrieve_forecast(names, res_pool[0])
        else:
            # multithreading forecast_pull
            n = int(math.ceil(len(names) / self.nthreads))
            prev_i = 0
            for i in range(self.nthreads):
                res_pool[i] = dict()
                next_i = self._inside(prev_i+n, len(names))
                p1 = names[prev_i:next_i]
                prev_i = next_i

                t = threading.Thread(
                        target=self.retrieve_forecast,
                        args=[p1, res_pool[i]],
                        name=f'{i}')
                t.start()
                thread_pool.append(t)

        # wait for threads giving updates
        it = 1
        while any(map(lambda x: x.is_alive(), thread_pool)):
            s_cnt = self._recursive_dict_len(res_pool)
            f_cnt = len(self.err_tracker)
            print(f'[{it}] -- {len(threading.enumerate())-1} JOBS ALIVE -- {s_cnt} SUCCESSFUL -- {f_cnt} FAILURES') if ((self.verbose > 0) and ((it-1) % 10 == 0)) else None
            it += 1
            # time.sleep(5)

        if len(self.err_tracker) > 0:
            print('Showing Error Dictionary:') if self.verbose > 0 else None
            self.pp.pprint(self.err_tracker) if self.verbose > 0 else None

        master = dict()
        for res in res_pool.values():
            master = {**master, **res}

        print(f'Found a total of {len(master)} forecasts!!') if self.verbose > 0 else None
        print(f'[ COMPLETE - ForecastRetrieval {self.nthreads}-threads ]###################') if self.verbose > 0 else None

        return master
