import unittest
from surfsup.maps import distance_miles


class TestMaps(unittest.TestCase):

    def test_approx(self) -> None:
        blacks = (32.877231, -117.25303)
        la_jolla = (32.863, -117.257)

        self.assertAlmostEqual(distance_miles(
            blacks[0], blacks[1], la_jolla[0], la_jolla[1]), 1.009704105)
