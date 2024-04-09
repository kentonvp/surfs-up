from math import pi, cos, asin, sqrt
from dataclasses import dataclass


@dataclass
class Location:
    latitude: float
    longitude: float

    def to_dict(self):
        return {"latitude": self.latitude, "longitude": self.longitude}


def _distance_miles(lat1: float, lon1: float, lat2: float, lon2: float):
    """Calculate the distance between two coordinates using Haversine formula.

    https://en.wikipedia.org/wiki/Haversine_formula"""
    p = pi / 180.0
    a = (
        0.5
        - cos((lat2 - lat1) * p) / 2
        + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    )

    return 3958 * 2 * asin(sqrt(a))


def distance_miles(location1: Location, location2: Location) -> float:
    return _distance_miles(
        location1.latitude, location1.longitude, location2.latitude, location2.longitude
    )
