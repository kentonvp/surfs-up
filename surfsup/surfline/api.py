import json

import requests
from bs4 import BeautifulSoup
from numpy import empty
from surfsup.login_info import LoginInfo
from surfsup.surfline.database import SpotRecord, SurflineSpotDB

Response = requests.models.Response

class SurflineAPI:
    session: requests.Session

    def __init__(self, db_name:str):
        self.database = SurflineSpotDB(db_name)
        self.session = requests.Session()

    def __del__(self):
        self.session.close()

    def authenticate_user(self, login:LoginInfo, s:requests.Session):
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

        resp = s.post(url_path, data=payload)
        assert resp.status_code == 200

        return json.loads(resp.text)

    def build_spot_url(self, spot_name:str) -> str:
        # This should go out to a 'database' and pull the NAME and ID given the
        # name.  Database is a loose word. We don't need massive storage and
        # this the values shouldn't change too much...So, might be worth
        # simplicity to have a manual CSV which we read in at the the top.
        # (lookup_db)
        spot_record = self.database.select(spot_name, by_att='name')
        return 'https://surfline.com/surf-report/blacks/5842041f4e65fad6a770883b'

    def spot_check(self, spot_url:str) -> dict:
        try:
            resp = self.session.get(spot_url)
            spot_data = self.parse_spot_check_response(resp)
            return spot_data
        except Exception as e:
            print('Exception trying to check spot: {}'.format(spot_url))
            print(e)


        return {}

    def multi_spot_check(self, spot_urls:list[str]) -> list[dict]:
        data = []

        for url in spot_urls:
            data.append(self.spot_check(url))

        return data

    def parse_spot_check_response(self, resp:Response) -> dict:
        soup = BeautifulSoup(resp.text, 'html.parser')

        # find the script which contains all the report data
        to_parse:str = soup.find_all('script')[13].string

        # parse to a python obj
        s_idx = to_parse.find('=') + 2
        all_surf_data = json.loads(to_parse[s_idx:])

        return all_surf_data['spot']['report']['data']

    def is_valid_report_url(self, link:str) -> bool:
        return '/surf-report/' in link

    def is_valid_parent_url(self, link:str) -> bool:
        return '/surf-reports-forecasts-cams/' in link

    def gather_spot_urls(self, starting_link:str) -> list[str]:
        resp = self.session.get(starting_link)

        soup = BeautifulSoup(resp.text, 'html.parser')
        all_a = soup.find_all('a')

        hrefs = []
        for link in all_a:
            tag_str = str(link)
            if 'href' in tag_str and (self.is_valid_report_url(tag_str) or self.is_valid_parent_url(tag_str)):
                href = link['href']
                hrefs.append(href)

        return hrefs

    def _generate_link_from_href(self, poss_href:str) -> str:
        if poss_href.startswith('/'):
            return 'https://www.surfline.com' + poss_href

        return poss_href

    def _parse_to_record(self, link:str, data:dict):
        rec_dict = {
            'name': data['spot']['name'],
            'spot_id': data['spot']['subregion']['_id'],
            'latitude': data['spot']['lat'],
            'longitude': data['spot']['lon'],
            'formal_name': data['spot']['name'],
            'url': link
        }
        return SpotRecord.from_dict(rec_dict)

    def search_for_urls_bfs(self, starting_link:str) -> list[str]:
        queue = [starting_link]

        seen = dict.fromkeys([str(u) for u in self.database.table['url']], True)
        errors = []
        count = 0
        while len(queue) > 0:
            print('queue at: {}; seen: {}; report-hits: {}'.format(len(queue), len(seen), count))
            curr_href = queue.pop(0)
            link = self._generate_link_from_href(curr_href)

            try:
                if link in seen:
                    continue

                if self.is_valid_report_url(link):
                    self.database.add_record(self._parse_to_record(link, self.spot_check(link)))
                    count += 1

                sub_hrefs = self.gather_spot_urls(link)
                queue.extend(sub_hrefs)
                seen[link] = True
            except Exception:
                print('Exception caught: {}'.format(link))
                errors.append(link)

        return errors
