import json

import requests
from typing import List, Dict
from bs4 import BeautifulSoup
from surfsup.login_info import LoginInfo
from surfsup.surfline.database import SurflineSpotDB

Response = requests.models.Response


class SurflineAPI:
    session: requests.Session
    database: SurflineSpotDB

    def __init__(self, db_name: str):
        """Create a surlfine with a connected database."""
        self.database = SurflineSpotDB(db_name)
        self.session = requests.Session()

    def __del__(self):
        """Close all connections to Surfline."""
        self.session.close()

    def authenticate_user(self, login: LoginInfo):
        """Authenticate the Surfline connection with a premium login."""
        url_path = 'https://services.surfline.com/trusted/token?isShortLived=false'
        payload = {
            'grant_type': 'password',
            'username': login.username,
            'password': login.password,
            'device_id': 'Safari-14.1.2',
            'device_type': 'Safari 14.1.2 on OS X 10.15.7',
            'forced': True,
            'authorizationString': 'Basic NWM1OWU3YzNmMGI2Y2IxYWQwMmJhZjY2OnNrX1FxWEpkbjZOeTVzTVJ1MjdBbWcz'
        }

        resp = self.session.post(url_path, data=payload)
        assert resp.status_code == 200

        return json.loads(resp.text)

    def valid_name(self, name: str) -> bool:
        return name in self.get_spot_names()

    def validate_names(self, names: list[str]):
        """Check if the names list of spot names are valid"""
        for n in names:
            if not self.valid_name(n):
                print(f'{n} is not a valid spot name')
                return False

        return True

    def get_spot_names(self) -> List[str]:
        return list(self.database.table['name'])

    def _build_spot_url(self, spot_name: str) -> str:
        spot_record = self.database.select(spot_name, by_att='name')
        return spot_record.url

    def spot_check(self, name: str) -> Dict:
        spot_url = self._build_spot_url(name)
        resp = self.session.get(spot_url)
        spot_data = self.format_report_response_data(resp)
        return spot_data

    def format_report_response_data(self, resp: Response) -> Dict:
        soup = BeautifulSoup(resp.text, 'html.parser')

        # find the script which contains all the report data
        script_tag = soup.find_all('script')[13]
        to_parse = str(script_tag.string)   # type: ignore

        # parse to a python obj
        s_idx = to_parse.find('=') + 2
        all_surf_data = json.loads(to_parse[s_idx:])

        return all_surf_data['spot']['report']['data']
