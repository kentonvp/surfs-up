import os
from pprint import PrettyPrinter

import requests

from surfsup.login_info import LoginInfo
from surfsup.surfline.api import SurflineAPI

login = LoginInfo()
db_name = os.path.join("surfsup", "surfline", "spot_lookups.csv")
surfline = SurflineAPI(login, db_name)

pp = PrettyPrinter(indent=4, width=500, compact=False)

mydata = None
with requests.Session() as s:
    surfline.authenticate_user(s)

    spot_url = surfline.build_spot_url("blacks")

    mydata = surfline.spot_check(s, spot_url)


pp.pprint(mydata)
