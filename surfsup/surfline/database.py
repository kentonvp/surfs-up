from dataclasses import asdict, dataclass
from os.path import exists

from surfsup.excepts import InvalidSchemaException

import pandas as pd


@dataclass
class SpotRecord:
    name:str
    spot_id:str
    latitude:float
    longitude:float
    formal_name:str
    url:str

    def get(self, name:str):
        return self.__dict__[name]

    @classmethod
    def from_dict(cls, rec_dict:dict):
        return cls(
            name = rec_dict["name"],
            spot_id = rec_dict["spot_id"],
            latitude = rec_dict["latitude"],
            longitude = rec_dict["longitude"],
            formal_name = rec_dict["formal_name"],
            url = rec_dict["url"])

    @classmethod
    def fields(cls) -> list[str]:
        return sorted(list(cls.__dict__['__dataclass_fields__'].keys()))

    @staticmethod
    def preferred_order() -> list[str]:
        return ['name','spot_id','latitude','longitude','formal_name','url']


class SurflineSpotDB:
    db_name: str
    table: pd.DataFrame

    def __init__(self, db_name:str):
        self.db_name = db_name
        if exists(db_name):
            self.table = pd.read_csv(db_name, index_col=False)
            if sorted(list(self.table.columns)) != SpotRecord.fields():
                raise InvalidSchemaException
        else:
            self.table = pd.DataFrame(columns=SpotRecord.fields())
            self.flush()

    def add_record(self, record:SpotRecord) -> None:
        self.table = self.table.append(asdict(record), ignore_index=True)

        self.flush()

    def del_record(self, record:SpotRecord) -> None:
        idx = self.__get_idx(record.name)
        self.table.drop([idx], inplace=True)

        self.flush()

    def select(self, val, by_att:str="name") -> SpotRecord:
        row_idx = self.__get_idx(val, by_att)
        rec_dict = self.table.iat(row_idx).to_dict()
        return SpotRecord.from_dict(rec_dict)

    def flush(self) -> None:
        self.table[SpotRecord.preferred_order()].to_csv(self.db_name, index=False)

    def __get_idx(self, val, by_att:str="name") -> int:
        return self.table[by_att].to_list().index(val)
