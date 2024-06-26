import os
import unittest
from unittest.mock import patch

from genericpath import exists
from surfsup.excepts import InvalidSchemaException
from surfsup.login_info import LoginInfo
from surfsup.surfline.api import SurflineAPI
from surfsup.surfline.database import SpotRecord, SurflineSpotDB
from surfsup.utils import joinpath


def test_joinpath(fname: str):
    return joinpath(os.getcwd(), "test", "testfiles", fname)


class TestSurflineSpotDB(unittest.TestCase):
    database: SurflineSpotDB
    fake_db: str

    # test constants
    TEST_DB_NAME = "init_fake_db.csv"
    TEST_DB_OUTPUT = "test_output.csv"
    TEST_TMP_DB = "no_file_with_this_name.csv"

    TEST_RECORD_ENTRY = SpotRecord.from_dict(
        {
            "name": "blackies",
            "spot_id": "somehash",
            "latitude": 32.12345,
            "longitude": 3.54321,
            "formal_name": "Blackies Pier",
            "url": "https://www.surfline.com/surf-report/blackies/somehash",
        }
    )
    TEST_RECORD_STR = "blackies,somehash,32.12345,3.54321,Blackies Pier,https://www.surfline.com/surf-report/blackies/somehash\n"

    def __init__(self, method_name: str) -> None:
        super().__init__(methodName=method_name)
        # initialize with a starter db
        self.database = SurflineSpotDB(test_joinpath(self.TEST_DB_NAME))

        # edit the output db so we can mutate during tests
        self.fake_db = test_joinpath(self.TEST_DB_OUTPUT)
        self.database.name = self.fake_db

        # flush to create the file
        self.database.flush()

    def setUp(self) -> None:
        super().setUp()
        self.database = SurflineSpotDB(test_joinpath(self.TEST_DB_NAME))
        self.database.name = self.fake_db

    def test_database_not_found(self) -> None:
        fname = test_joinpath(self.TEST_TMP_DB)
        self.assertFalse(exists(fname))
        SurflineSpotDB(fname)
        self.assertTrue(exists(fname))

    def test_invalid_database(self) -> None:
        with self.assertRaises(InvalidSchemaException):
            SurflineSpotDB(test_joinpath("invalid_schema.csv"))

    def test_load_database(self):
        self.assertIsInstance(self.database, SurflineSpotDB)

    def test_add_record(self):
        rec = self.TEST_RECORD_ENTRY
        self.database.add_record(rec)

        f1 = open(self.fake_db)
        recently_added = f1.readlines()[-1]
        f1.close()
        self.assertEqual(recently_added, self.TEST_RECORD_STR)

    def test_del_record(self):
        rec = self.TEST_RECORD_ENTRY
        self.database.add_record(rec)
        self.database.del_record(rec)

        f1 = open(self.fake_db)
        recently_added = f1.readlines()[-1]
        f1.close()
        self.assertNotEqual(recently_added, self.TEST_RECORD_STR)

    def test_select_record(self):
        rec = self.TEST_RECORD_ENTRY
        self.database.add_record(rec)

        rec2 = SpotRecord.from_dict(
            {
                "name": "blackies2",
                "spot_id": "somehash2",
                "latitude": 32.123452,
                "longitude": 3.543212,
                "formal_name": "Blackies Pier2",
                "url": "https://www.surfline.com/surf-report/blackies/somehash2",
            }
        )
        self.database.add_record(rec2)

        self.assertEqual(len(self.database.table), 3)

        lookup_rec = self.database.select("blackies")
        lookup_rec2_by_att = self.database.select("somehash2", by_att="spot_id")

        self.assertEqual(lookup_rec, rec)
        self.assertEqual(lookup_rec2_by_att, rec2)
        self.assertNotEqual(lookup_rec, lookup_rec2_by_att)

    def tearDown(self) -> None:
        fnames = [self.TEST_TMP_DB, self.TEST_DB_OUTPUT]
        to_remove = [test_joinpath(x) for x in fnames]
        for fname in to_remove:
            if exists(fname):
                os.remove(fname)

        return super().tearDown()


class TestSurflineAPI(unittest.TestCase):
    TEST_DB_NAME = "init_fake_db.csv"
    TEST_TMP_DB = "tmp_database.csv"

    def test_finds_database(self):
        database_fname = test_joinpath(self.TEST_DB_NAME)
        surfline = SurflineAPI(database_fname)
        self.assertTrue(surfline.database.name, database_fname)

    def test_creates_new_database(self):
        database_fname = test_joinpath(self.TEST_TMP_DB)
        SurflineAPI(database_fname)
        self.assertTrue(exists(database_fname))

    def test_authenticates_user_success(self):
        database_fname = test_joinpath(self.TEST_TMP_DB)
        surfline = SurflineAPI(database_fname)

        login = LoginInfo("foo", "foobar")

        with patch("surfsup.surfline.api.HTMLSession.post") as mock_resp:
            mock_resp.return_value.status_code = 200
            mock_resp.return_value.text = '{"access_token":"123jllkj12313","refresh_token":"123jklk123l12h3l1j2","expires_in":2592000,"token_type":"Bearer"}'
            res = surfline.authenticate_user(login)

            self.assertSetEqual(
                set(res.keys()),
                set(["access_token", "refresh_token", "expires_in", "token_type"]),
            )

    def test_user_authentication_failure(self):
        database_fname = test_joinpath(self.TEST_TMP_DB)
        surfline = SurflineAPI(database_fname)

        login = LoginInfo("foo", "foobar")

        with self.assertRaises(AssertionError):
            surfline.authenticate_user(login)

    def test_validate_names_check_happy(self):
        database_fname = test_joinpath(self.TEST_DB_NAME)
        surfline = SurflineAPI(database_fname)
        self.assertTrue(surfline.validate_names(["Blacks"]))

    def test_valididate_names_check_unhappy(self):
        database_fname = test_joinpath(self.TEST_DB_NAME)
        surfline = SurflineAPI(database_fname)
        self.assertFalse(surfline.validate_names(["UnicornLand123", "Blackies"]))

    def test_spot_data_retreival(self):
        database_fname = test_joinpath(self.TEST_DB_NAME)
        surfline = SurflineAPI(database_fname)

        data = surfline.spot_check("Blacks")
        self.assertSetEqual(set(data.keys()), set(["spot", "report", "forecast"]))

    def tearDown(self) -> None:
        fnames = [self.TEST_TMP_DB]
        to_remove = [test_joinpath(x) for x in fnames]
        for fname in to_remove:
            if exists(fname):
                os.remove(fname)

        return super().tearDown()
