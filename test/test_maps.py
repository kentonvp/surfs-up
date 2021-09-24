import unittest
from surfsup.maps import Location, distance_miles


class TestMaps(unittest.TestCase):

    def test_approx(self) -> None:
        blacks = Location(32.877231, -117.25303)
        la_jolla = Location(32.863, -117.257)

        self.assertAlmostEqual(distance_miles(blacks, la_jolla), 1.009704105)
        self.assertAlmostEqual(distance_miles(la_jolla, blacks), 1.009704105)
