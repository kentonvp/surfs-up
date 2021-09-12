import json
from surfsup.surfline.database import SurflineSpotDB
import time

import requests
from bs4 import BeautifulSoup

from surfsup.login_info import LoginInfo

Response = requests.models.Response

class SurflineAPI:
    session: requests.Session

    def __init__(self, login:LoginInfo, db_name:str):
        self.lookup_db = SurflineSpotDB(db_name)
        self.session = requests.Session()
        self.authenticate_user(login, self.session)

    def __del__(self):
        self.session.close()

    def authenticate_user(self, login:LoginInfo, s:requests.Session) -> Response:
        url_path = "https://services.surfline.com/trusted/token?isShortLived=false"
        payload = {
            "grant_type": "password",
            "username": login.username,
            "password": login.password,
            "device_id": "Safari-14.1.2",
            "device_type": "Safari 14.1.2 on OS X 10.15.7",
            "forced": True,
            "authorizationString": "Basic NWM1OWU3YzNmMGI2Y2IxYWQwMmJhZjY2OnNrX1FxWEpkbjZOeTVzTVJ1MjdBbWcz"
        }

        resp = s.post(url_path, data=payload)

        return resp

    def build_spot_url(self, spot_name:str) -> str:
        # This should go out to a "database" and pull the NAME and ID given the
        # name.  Database is a loose word. We don't need massive storage and
        # this the values shouldn't change too much...So, might be worth
        # simplicity to have a manual CSV which we read in at the the top.
        # (lookup_db)
        spot_record = self.lookup_db.select(spot_name, by_att="name")
        return "https://surfline.com/surf-report/blacks/5842041f4e65fad6a770883b"


    def spot_check(self, spot_url:str) -> dict:
        resp = self.session.get(spot_url)
        spot_data = self.parse_spot_check_response(resp)
        return spot_data


    def multi_spot_check(self, spot_urls):
        data = []

        for url in spot_urls:
            data.append(self.spot_check(url))

        return data

    def parse_spot_check_response(self, resp:Response) -> dict:
        soup = BeautifulSoup(resp.text, "html.parser")

        # find the script which contains all the report data
        to_parse:str = soup.find_all("script")[13].string

        # parse to a python obj
        s_idx = to_parse.find('=') + 2
        all_surf_data = json.loads(to_parse[s_idx:])

        return all_surf_data['spot']['report']['data']


    def is_valid_spot_url(self, link:str) -> bool:
        return '/surf-report/' in link


    def gather_spot_urls(self, page:str):
        resp = self.session.get(page)

        soup = BeautifulSoup(resp.text, 'html.parser')
        all_a = soup.find_all('a')

        hrefs = []
        for link in all_a:
            if 'href' in str(link) and self.is_valid_spot_url(str(link)):
                href = link['href']
                hrefs.append(href)

        return hrefs
