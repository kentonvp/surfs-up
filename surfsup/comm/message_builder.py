from surfsup.surfline.api import SurflineAPI
from surfsup.utils import joinpath
from surfsup.maps import Location


class MessageBuilder:
    def __init__(self):
        self.surfline = SurflineAPI(joinpath('data', 'spot_lookups.csv'))

    def is_spot(self, spot_name: str) -> bool:
        """Return if message text indicates a spot name."""
        return self.surfline.valid_name(spot_name)

    def clean(self, obj: dict) -> str:
        value = obj['conditions']['value']
        surf_min = obj['waveHeight']['min']
        surf_max = obj['waveHeight']['max']
        surf_rel = obj['waveHeight']['humanRelation']
        return f'Surf Report: {value}\nSurf is {surf_min}ft to {surf_max}ft and is {surf_rel.lower()}.\nHave fun!'

    def build_report_message(self, spot_name: str) -> str:
        if not self.surfline.valid_name(spot_name):
            # spell check call and print message with possible correct version
            # if 98% valide:
            #   spot_name = correct_spot_name
            # else:
            #   next step
            possible_corrections = ['i', 'dont', 'know', 'yet']
            return f'ERROR: {spot_name} was invalid. Did you mean: {possible_corrections}'
        report_data = self.surfline.spot_check(spot_name)
        new_message = self.clean(report_data['forecast'])
        return new_message
    
    def build_report_message_for_location(self, loc: Location):
        return f'Your location is at ({loc.longitude}, {loc.latitude})!!!'
        # names = surfline.lookup_spot_by_location(user_loc)
        # fcst_fetcher = ForecastFetcher(db_name)
        # fcst_dictionary = fcst_fetcher.runner(user_loc, max_radius=50)
        # top5 = sort(fcst_dictionary)
        # return  msg=messenger.build_report_message_for_location(top5)

