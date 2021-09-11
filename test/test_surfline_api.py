import os
import unittest
from shutil import copy

from genericpath import exists
from surfsup.excepts import InvalidSchemaException
from surfsup.surfline.database import SpotRecord, SurflineSpotDB


def joinpath(fname:str) -> str:
    return os.path.join("test", "testfiles", fname)


class TestSurflineSpotDB(unittest.TestCase):
    database: SurflineSpotDB
    fake_db: str

    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        # initialize with a starter db
        self.database = SurflineSpotDB(joinpath("init_fake_db.csv"))

        # edit the output db so we can mutate during tests
        self.fake_db = joinpath("test_output.csv")
        self.database.db_name = self.fake_db

        # flush to create the file
        self.database.flush()

    def setUp(self) -> None:
        self.database = SurflineSpotDB(self.fake_db)


    def test_database_not_found(self) -> None:
        fname = joinpath("no_file_with_this_name.csv")
        self.assertFalse(exists(fname))
        SurflineSpotDB(fname)
        self.assertTrue(exists(fname))

    def test_invalid_database(self) -> None:
        with self.assertRaises(InvalidSchemaException):
            SurflineSpotDB(joinpath("invalid_schema.csv"))

    def test_load_database(self):
        self.assertIsInstance(self.database, SurflineSpotDB)

    def test_add_record(self):
        rec = SpotRecord.from_dict({
            'name': 'blackies',
            'spot_id': 'somehash',
            'latitude': 32.12345,
            'longitude': 3.54321,
            'formal_name': 'Blackies Pier',
            'url': '/surf-report/blackies/somehash'
        })
        self.database.add_record(rec)

        f1 = open(self.fake_db)
        recently_added = f1.readlines()[-1]
        f1.close()
        self.assertEqual(recently_added, "blackies,somehash,32.12345,3.54321,Blackies Pier,/surf-report/blackies/somehash\n")

    def test_del_record(self):
        rec = SpotRecord.from_dict({
            'name': 'blackies',
            'spot_id': 'somehash',
            'latitude': 32.12345,
            'longitude': 3.54321,
            'formal_name': 'Blackies Pier',
            'url': '/surf-report/blackies/somehash'
        })
        self.database.add_record(rec)
        self.database.del_record(rec)

        f1 = open(self.fake_db)
        recently_added = f1.readlines()[-1]
        f1.close()
        self.assertNotEqual(recently_added, "blackies,somehash,32.12345,3.54321,Blackies Pier,/surf-report/blackies/somehash\n")

    def test_select_record(self):
        pass

    def tearDown(self) -> None:
        to_remove = [joinpath(x) for x in ["no_file_with_this_name.csv", "test_output.csv"]]
        for fname in to_remove:
            if exists(fname):
                os.remove(fname)


if __name__ == '__main':
    unittest.main()
