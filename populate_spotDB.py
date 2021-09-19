import os

import requests
from bs4 import BeautifulSoup

from surfsup.surfline.api import SurflineAPI
from surfsup.surfline.database import SpotRecord
from surfsup.utils import joinpath


def is_valid_report_url(link: str) -> bool:
    return '/surf-report/' in link


def is_valid_region_url(link: str) -> bool:
    return '/surf-reports-forecasts-cams/' in link


def gather_spot_urls(resp: requests.Response) -> list[str]:
    soup = BeautifulSoup(resp.text, 'html.parser')
    all_a = soup.find_all('a')

    hrefs = []
    for link in all_a:
        tag_str = str(link)
        if 'href' in tag_str and (is_valid_report_url(tag_str) or is_valid_region_url(tag_str)):
            href = link['href']
            hrefs.append(href)

    return hrefs


def generate_link_from_href(possible_href: str) -> str:
    if possible_href.startswith('/'):
        return 'https://www.surfline.com' + possible_href

    return possible_href


def report_data_to_record(link: str, data: dict):
    rec_dict = {
        'name': data['spot']['name'],
        'spot_id': data['spot']['subregion']['_id'],
        'latitude': data['spot']['lat'],
        'longitude': data['spot']['lon'],
        'formal_name': data['spot']['name'],
        'url': link
    }
    return SpotRecord.from_dict(rec_dict)


def populate_spot_database(db_name: str, starting_link: str = "https://www.surfline.com") -> list[str]:
    """BFS for new surf report urls.

    Search for new surf report urls and add them to the supplied database.
    Returns a list of urls which could not be processed.

    Keyword arguments:
    starting_link -- the url link to the starting page (default https://www.surfline.com)
    """
    surfline = SurflineAPI(db_name)
    queue = [starting_link]

    seen = dict.fromkeys([str(u)
                          for u in surfline.database.table['url']], True)
    errors = []
    count = 0
    while len(queue) > 0:
        print(
            'queue at: {}; seen: {}; report-hits: {}'.format(len(queue), len(seen), count))
        curr_href = queue.pop(0)
        link = generate_link_from_href(curr_href)

        try:
            if link in seen:
                continue

            if is_valid_report_url(link):
                surfline.database.add_record(
                    report_data_to_record(link, surfline.spot_check(link)))
                count += 1

            resp = requests.get(link)
            sub_hrefs = gather_spot_urls(resp)
            queue.extend(sub_hrefs)
            seen[link] = True
        except Exception:
            print('Exception caught: {}'.format(link))
            errors.append(link)

    return errors


def main():
    cwd = os.getcwd()
    database_name = joinpath(cwd, 'data', 'spot_lookups.csv')
    errors = populate_spot_database(
        database_name, 'https://www.surfline.com/surf-report/')

    # print errors to a file
    with open('error_urls.txt', 'a+') as fname:
        for err_url in errors:
            fname.write(err_url + "\n")


if __name__ == '__main__':
    main()
