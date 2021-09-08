from dataclasses import asdict, dataclass
from os.path import exists

import pandas as pd


@dataclass
class SpotRecord:
    name:str
    spot_id:int
    location:tuple

    def get(self, name:str):
        return self.__dict__[name]


class SurflineSpotDB:
    db_name: str
    table: pd.DataFrame

    def __init__(self, db_name:str):
        if exists(db_name):
            self.table = pd.read_csv(db_name)
            assert sorted(list(self.table.columns)) == sorted(["name", "spot_id", "location"])
        else:
            self.table = pd.DataFrame(columns=["name", "spot_id", "location"])
            self.flush()


    def add_record(self, record:SpotRecord) -> None:
        self.table = self.table.append(asdict(record), ignore_index=True)

        self.flush()
        return None


    def del_record(self, record:SpotRecord) -> None:
        idx = self.__get_idx(record.name)
        self.table.drop([idx], inplace=True)

        self.flush()
        return None


    def select(self, val, by_att:str="name") -> SpotRecord:
        row_idx = self.__get_idx(val, by_att)
        rec_dict = self.table.iat(row_idx).to_dict()
        return self.__build_record(rec_dict)


    def flush(self) -> None:
        self.table.to_csv(self.db_name, index=False)
        return None


    def __get_idx(self, val, by_att:str="name") -> int:
        return self.table[by_att].to_list().index(val)


    def __build_record(self, rec_dict:dict) -> SpotRecord:
        name = rec_dict["name"]
        spot_id = rec_dict["spot_id"]
        location = rec_dict["location"]
        return SpotRecord(name, spot_id, location)
