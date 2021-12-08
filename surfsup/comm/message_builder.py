from surfsup.dto.forecast_parser import ForecastFetcher
from surfsup.comm.str_constants import SURFSUP_USAGE_MSG
from surfsup.utils import joinpath
from surfsup.maps import Location
import math
from surfsup.comm.markdown import gen_link, fmt_text


class MessageBuilder:
    forecast_fetcher: ForecastFetcher

    def __init__(self):
        db_path = joinpath('data', 'spot_lookups.csv')
        self.forecast_fetcher = ForecastFetcher(db_path)

    def is_spot(self, spot_name: str) -> bool:
        """Return if message text indicates a spot name."""
        return self.forecast_fetcher.surfline.valid_name(spot_name)

    def clean(self, obj: dict) -> str:
        value = obj['conditions']['value']
        surf_min = obj['waveHeight']['min']
        surf_max = obj['waveHeight']['max']
        surf_rel = obj['waveHeight']['humanRelation']
        return f'Surf Report: {self.get_emoji(value)} {value}\n' + \
            f'Surf is {surf_min}ft to {surf_max}ft, {surf_rel.lower()}.\n' + \
            'Have fun!'

    def build_report_message(self, spot_name: str) -> str:
        spot_name = self.normalize_spot_name(spot_name)
        if not self.is_spot(spot_name):
            if spot_name.lower() == 'help':
                return SURFSUP_USAGE_MSG
            possible_corrections = self.forecast_fetcher.partial_name(spot_name)
            return f'ERROR: {spot_name} was invalid. Possible corrections:\n' + \
                    '\n'.join(possible_corrections) + \
                    '\nDid you need /help' + '?'

        report_data = self.forecast_fetcher.surfline.spot_check(spot_name)
        new_message = self.clean(report_data['forecast'])
        return new_message

    def spot_message_fmt(self, obj):
        return self.__format_nameline(obj) + \
                self.__format_scoreline(obj) + \
                self.__format_conditionsline(obj) + \
                self.__format_wavesizeline(obj) + \
                self.__format_windline(obj)

    def build_report_message_for_location(self, loc: Location, max_radius: int, max_height: int):
        fcst_results, distances, urls = self.forecast_fetcher.by_loc(loc, max_radius)
        best_fcsts = self.forecast_fetcher.top_sorted(fcst_results, max_height, n=5)

        def mk_dict(row):
            other_info = {'distance': distances[row['name']], 'url': urls[row['name']], 'max_height': max_height}
            return {**row.to_dict(), **other_info}

        return '\n'.join([self.spot_message_fmt(mk_dict(spot)) for _, spot in best_fcsts.iterrows()])

    def replace_apostrophe_lookalikes(self, spot_name: str) -> str:
        # grave accent (U+0060), open signle quote (U+2018), close single quote (U+2019)
        return spot_name.replace("`", "'") \
                .replace("‘", "'") \
                .replace("’", "'")

    def normalize_spot_name(self, spot_name: str) -> str:
        out = self.replace_apostrophe_lookalikes(spot_name)
        return out

    def get_emoji(self, condition: str):
        if not condition or condition.lower() in ['flat', 'very_poor']:
            return '\U0001F4A9\U0001F634' # poop + sleeping in bed
        if condition.lower() in ['poor']:
            return '\U0001F643' # upside down smile
        if condition.lower() in ['poor_to_fair']:
            return '\U0001F974' # woozy face
        if condition.lower() in ['fair']:
            return '\U0001F610' # neutral smile
        if condition.lower() in ['fair_to_good']:
            return '\U0001F60A' # smile
        if condition.lower() in ['good']:
            return '\U0001F64C' # praise hands
        if condition.lower() in ['good_to_epic', 'epic']:
            return '\U0001F924\U0001F4A6\U0001F4A3' # drooling + sweat drops + bomb
        return '\U0001F4A9' # poop

    def get_approx_direction(self, direction):
        directions = ["N \U00002193", "NE \U00002199", "E \U00002B05", "SE \U00002196", "S \U00002B06", "SW \U00002197", "W \U000027A1", "NW \U00002198"]
        degs = [0, 45, 90, 135, 180, 225, 275, 315]

        one16 = 22.5 # one16 of a circle 360 degrees
        if direction > degs[-1] + one16:
            return directions[0]

        for i in range(1,len(degs)):
            if degs[i-1] <= direction < degs[i]:
                if degs[i] - direction < direction - degs[i-1]:
                    nearest = i
                else:
                    nearest = i-1
                break

        return directions[nearest]

    def get_size_emoji(self, height, max_height):
        if height < max_height - 1:
            return "\U0001F535" # blue circle
        if height < max_height + 1:
            return "\U0001F7E2" # green circle
        return "\U0001F534"

    def __format_nameline(self, obj):
        namelink = gen_link(obj['name'], obj['url'])
        distance = round(obj['distance'], 2)
        return namelink + fmt_text(f" ({distance}mi)\n")

    def __format_scoreline(self, obj):
        val = round(obj['sortable'], 4)
        return fmt_text(f"ScoreValue: {val}\n")

    def __format_conditionsline(self, obj):
        emoji = self.get_emoji(obj['conditions'])
        conds = obj['conditions'].lower() if obj['conditions'] else "None"
        return fmt_text(f"Cond: {emoji} {conds}\n")

    def __format_wavesizeline(self, obj):
        ave_height = (obj['wave_max']+obj['wave_min'])/2.0
        emoji = self.get_size_emoji(ave_height, obj['max_height'])

        occ = "\n"
        if obj['wave_occ'] and not math.isnan(obj['wave_occ']):
            occ = f" (occ. {obj['wave_occ']})\n"

        wave_range = f"{obj['wave_min']}-{obj['wave_max']}"
        return fmt_text(f"Wave size: {emoji} {wave_range}{occ}")

    def __format_windline(self, obj):
        speed = obj['wind_speed']
        emoji = self.get_approx_direction(obj['wind_dir'])
        direction = round(obj['wind_dir'], 2)
        return fmt_text(f"Wind: {speed}mph {emoji} {direction}\n")
