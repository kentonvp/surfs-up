from surfsup.dto.forecast_parser import ForecastFetcher
from surfsup.utils import joinpath
from surfsup.maps import Location


class MessageBuilder:
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
        return f'Surf Report: {value}\nSurf is {surf_min}ft to {surf_max}ft and is {surf_rel.lower()}.\nHave fun!'

    def build_report_message(self, spot_name: str) -> str:
        spot_name = self.normalize_apostrophe_chars(spot_name)
        if not self.is_spot(spot_name):
            possible_corrections = ['i', 'dont', 'know', 'yet']
            return f'ERROR: {spot_name} was invalid. Did you mean: {possible_corrections}'

        report_data = self.forecast_fetcher.surfline.spot_check(spot_name)
        new_message = self.clean(report_data['forecast'])
        return new_message

    def build_report_message_for_location(self, loc: Location, max_radius: int, max_height: int):
        fcst_results, distances = self.forecast_fetcher.by_loc(loc, max_radius)
        best_fcsts = self.forecast_fetcher.top_sorted(fcst_results, max_height, n=5)
        def fmt_spot(row):
            return f"Name: {row['name']}\nDistance: {distances[row['name']]}\nSortValue: {row.sortable}\nCond: {row.conditions}\nWind: ({row.wind_speed},{row.wind_dir})\nWaves:{row.wave_min}-{row.wave_max}({row.wave_occ})\nSwell:{row.swell_dir}\n"

        return '\n'.join([fmt_spot(spot) for _, spot in best_fcsts.iterrows()])

    def normalize_apostrophe_chars(self, spot_name: str) -> str:
        validated_name = spot_name.replace("`", "'")
        validated_name = validated_name.replace("’", "'")
        return validated_name
