from dataclasses import dataclass
from typing import Any

@dataclass
class ConditionRecord:
    human: bool
    value: str
    expired: bool

    def as_csv(self, sep: str = ',') -> str:
        return sep.join([str(self.value)])


@dataclass
class WindRecord:
    speed: int
    direction: float

    def as_csv(self, sep: str = ',') -> str:
        return sep.join([str(self.speed), str(self.direction)])


@dataclass
class WaveHeightRecord:
    human: bool
    min: float
    max: int
    occasional: Any
    human_relation: str
    plus: bool

    def as_csv(self, sep: str = ',') -> str:
        return sep.join([str(self.min), str(self.max), str(self.occasional)])


@dataclass
class SwellRecord:
    height: float
    period: int
    direction: float
    direction_min: float

    def as_csv(self, sep: str = ',') -> str:
        return sep.join([str(self.height), str(self.period), str(self.direction)])


@dataclass
class TideRecord:
    type_: str
    height: float
    timestamp: int
    utc_offset: int

    def as_csv(self, sep: str = ',') -> str:
        return sep.join([str(self.height), str(self.timestamp)])


@dataclass
class TideCollectionRecord:
    previous: TideRecord
    current: TideRecord
    next: TideRecord

    def as_csv(self, sep: str = ',') -> str:
        return sep.join([self.previous.as_csv(sep), self.current.as_csv(sep), self.next.as_csv(sep)])


@dataclass
class WeatherRecord:
    water_min: int
    water_max: int
    temperature: int
    condition: str

    def as_csv(self, sep: str = ',') -> str:
        return sep.join([str(self.temperature), str(self.water_min), str(self.water_max)])


@dataclass
class ForecastRecord:
    note: str
    conditions: Any
    wind: Any
    swells: Any
    wave_height: Any
    tide: Any
    weather: Any
    
    def as_csv(self, sep: str = ',') -> str:
        return sep.join([
                self.conditions.as_csv(sep) if self.conditions != None else '',
                self.wind.as_csv(sep) if self.wind != None else ',',
                self.wave_height.as_csv(sep) if self.wave_height != None else ',,',
                self.swells[0].as_csv(sep) if self.swells[0] != None else ',,',
                self.tide.as_csv(sep) if self.tide != None else ',,,,,',
                self.weather.as_csv(sep)] if self.weather != None else ',,')

