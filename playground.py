import os
from pprint import PrettyPrinter

from bs4 import BeautifulSoup

from surfsup.login_info import LoginInfo
from surfsup.surfline.api import SurflineAPI

login = LoginInfo(os.environ["SURFLINE_USERNAME"], os.environ["SURFLINE_PASSWORD"])
db_name = os.path.join("surfsup", "surfline", "spot_lookups.csv")
surfline = SurflineAPI(login, db_name)

pp = PrettyPrinter(indent=4, width=500, compact=False)

mydata = None
resp = surfline.authenticate_user(login, surfline.session)

urls = surfline.gather_spot_urls('https://www.surfline.com/surf-forecasts/north-san-diego/58581a836630e24c44878fd7')
print(urls)

formatted = ["https://www.surfline.com" + url for url in urls]
print(formatted)

all_data = surfline.multi_spot_check(formatted)
print(all_data)
print('lenth: {}'.format(len(all_data)))