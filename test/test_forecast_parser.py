from genericpath import exists
import os
import unittest
from pprint import PrettyPrinter

from surfsup.dto.forecast_parser import ForecastFetcher, or_none
from surfsup.dto.forecast_dto import *
from surfsup.utils import joinpath


def test_joinpath(fname: str):
    return joinpath(os.getcwd(), 'test', 'testfiles', fname)


class TestForecastParser(unittest.TestCase):
    forecast_fetcher: ForecastFetcher
    pp = PrettyPrinter(indent=2)

    # test_constants
    TEST_DB_NAME = test_joinpath('sm_fake_db.csv')
    TMP_CSV_NAME = test_joinpath('tmp_csv.csv')

    def __init__(self, method_name: str) -> None:
        super().__init__(methodName=method_name)

    def setUp(self) -> None:
        self.forecast_fetcher = ForecastFetcher(self.TEST_DB_NAME)

    def test_empty_runner(self):
        forecasts = self.forecast_fetcher.runner()
        self.assertEqual(len(self.forecast_fetcher.surfline.get_spot_names()), len(forecasts))

    def test_small_runner(self):
        names: list[str] = [
            'Blackies','Blacks','La Jolla Shores'
            ]
        forecasts = self.forecast_fetcher.runner(names)
        self.assertEqual(3, len(forecasts))

    def test_csv_export(self):
        csv_name = test_joinpath(self.TMP_CSV_NAME)
        
        names: list[str] = [
            'Blackies','Blacks','La Jolla Shores'
            ]
        forecasts = self.forecast_fetcher.runner(names)

        self.forecast_fetcher.to_csv(csv_name, forecasts)
        self.assertTrue(exists(csv_name))

    def test_or_none_happy(self):
        self.assertEqual(24, or_none('name', lambda x: x + 1, 23))

    def test_or_none_unhappy(self):
        self.assertEqual(None, or_none('name', lambda x: x / 0 , 23))

    def tearDown(self) -> None:
        if exists(self.TMP_CSV_NAME):
            os.remove(self.TMP_CSV_NAME)

        return super().tearDown()

