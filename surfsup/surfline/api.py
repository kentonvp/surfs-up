import json
import traceback

from requests_html import HTMLResponse, HTMLSession
from surfsup.login_info import LoginInfo
from surfsup.surfline.database import SurflineSpotDB
from cachetools import cached, TTLCache


class SurflineAPI:
    session: HTMLSession
    database: SurflineSpotDB

    def __init__(self, db_name: str):
        """Create a surlfine with a connected database."""
        self.database = SurflineSpotDB(db_name)
        self.session = HTMLSession()

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

    def get_spot_names(self) -> list[str]:
        return list(self.database.table['name'])

    def _build_spot_url(self, spot_name: str) -> str:
        spot_record = self.database.select(spot_name, by_att='name')
        return spot_record.url

    @cached(cache=TTLCache(maxsize=1024, ttl=60*5))
    def spot_check(self, name: str) -> dict:
        spot_url = self._build_spot_url(name)
        resp: HTMLResponse = self.session.get(spot_url)
        i = 0
        while not resp.ok and i < 10:
            resp: HTMLResponse = self.session.get(spot_url)
            i += 1
        spot_data = self.format_report_response_data(resp)
        return spot_data

    def format_report_response_data(self, resp: HTMLResponse) -> dict:
        try:
            scripts = resp.html.element('script')
            # with open("data/making_resp.html", "w+") as f:
            #     f.write(resp.text)

            # find the script which contains all the report data
            script_tag = scripts[39]
            to_parse = str(script_tag.text)   # type: ignore

            # parse to a python obj
            # s_idx = to_parse.find('=') + 2
            all_surf_data = json.loads(to_parse)

            return all_surf_data['props']['pageProps']['ssrReduxState']['spot']['report']['data']
        except Exception:
            print('Surfline might have changed their response!!!! (format_report_response_data())')
            return {}
