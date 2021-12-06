from surfsup.dto.forecast_parser import ForecastFetcher
from surfsup.comm.str_constants import SURFSUP_USAGE_MSG
from surfsup.utils import joinpath
from surfsup.maps import Location
import math


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
        return f'Surf Report: {value}\n' + \
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
                    '\nDid you need /help ?'

        report_data = self.forecast_fetcher.surfline.spot_check(spot_name)
        new_message = self.clean(report_data['forecast'])
        return new_message

    def build_report_message_for_location(self, loc: Location, max_radius: int, max_height: int):
        fcst_results, distances = self.forecast_fetcher.by_loc(loc, max_radius)
        best_fcsts = self.forecast_fetcher.top_sorted(fcst_results, max_height, n=5)
        def fmt_spot(row):
            return f"Name: {row['name']}\n" + \
                    f"Distance: {round(distances[row['name']], 2)}\n" + \
                    f"SortValue: {round(row.sortable, 4)}\n" + \
                    f"Cond: {row.conditions}\n" + \
                    f"Wave size: {row.wave_min}-{row.wave_max}" + \
                        str(f" ({row.wave_occ})\n" if not math.isnan(row.wave_occ) else "\n") + \
                    f"Wind: (Speed: {row.wind_speed}, Dir: {round(row.wind_dir, 2)})\n" + \
                    f"Swell Dir: {round(row.swell_dir, 2)}\n"

        return '\n'.join([fmt_spot(spot) for _, spot in best_fcsts.iterrows()])

    def replace_apostrophe_lookalikes(self, spot_name: str) -> str:
        out = spot_name.replace("`", "'")    # replace grave accent (U+0060)
        out = out.replace("‘", "'")   # replace open signle quote (U+2018)
        out = out.replace("’", "'")   # replace close single quote (U+2019)
        return out

    def normalize_spot_name(self, spot_name: str) -> str:
        out = self.replace_apostrophe_lookalikes(spot_name)
        return out