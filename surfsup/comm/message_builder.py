import json
import os

from surfsup.surfline.api import SurflineAPI
from surfsup.utils import joinpath


class MessageBuilder:
    def __init__(self):
        self.surfline = SurflineAPI(joinpath('data', 'spot_lookups.csv'))

    def is_spot(self, spot_name: str) -> bool:
        """Return if message text indicates a spot name."""
        return spot_name in list(self.surfline.database.table['name'])

    def clean(self, obj: dict) -> str:
        value = obj['conditions']['value']
        surf_min = obj['waveHeight']['min']
        surf_max = obj['waveHeight']['max']
        surf_rel = obj['waveHeight']['humanRelation']
        return f'Surf Report: {value}\nSurf is {surf_min}ft to {surf_max}ft and is {surf_rel.lower()}.\nHave fun!'

    def build_report_message(self, spot_name: str) -> str:
        spot_url = self.surfline.build_spot_url(spot_name)
        report_data = self.surfline.spot_check(spot_url)
        new_message = self.clean(report_data['forecast'])
        return new_message
