from math import pi, cos, asin, sqrt


def distance_miles(lat1: float, lon1: float, lat2: float, lon2: float):
    """Calculate the distance between two coordinates using Haversine formula.

    https://en.wikipedia.org/wiki/Haversine_formula"""
    p = pi/180.0
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * \
        cos(lat2*p) * (1-cos((lon2-lon1)*p))/2

    return 3958*2 * asin(sqrt(a))
