from genericpath import exists
import os
import unittest
from pprint import PrettyPrinter
from unittest.mock import patch

from surfsup.dto.forecast_parser import ForecastFetcher, or_none
from surfsup.dto.forecast_dto import *
from surfsup.utils import joinpath


def test_joinpath(fname: str):
    return joinpath(os.getcwd(), "test", "testfiles", fname)


class TestForecastParser(unittest.TestCase):
    forecast_fetcher: ForecastFetcher
    pp = PrettyPrinter(indent=2)

    # test_constants
    TEST_DB_NAME = test_joinpath("sm_fake_db.csv")
    TMP_CSV_NAME = test_joinpath("tmp_csv.csv")
    TEST_FORECAST_RESP = {}

    def __init__(self, method_name: str) -> None:
        super().__init__(methodName=method_name)

    def setUp(self) -> None:
        self.forecast_fetcher = ForecastFetcher(self.TEST_DB_NAME)

    def test_empty_runner(self):
        with patch("surfsup.surfline.api.SurflineAPI.spot_check") as mock_obj:
            mock_obj.return_value = self.fake_spot_check_response()
            forecasts = self.forecast_fetcher.runner()
            self.assertEqual(
                len(self.forecast_fetcher.surfline.get_spot_names()),
                len(forecasts) + len(self.forecast_fetcher.err_tracker),
            )

    def test_small_runner(self):
        names: list[str] = ["Blackies", "Blacks", "La Jolla Shores"]
        forecasts = self.forecast_fetcher.runner(names)
        self.assertEqual(3, len(forecasts))

    def test_csv_export(self):
        csv_name = test_joinpath(self.TMP_CSV_NAME)

        names: list[str] = ["Blackies", "Blacks", "La Jolla Shores"]
        forecasts = self.forecast_fetcher.runner(names)

        self.forecast_fetcher.to_csv(csv_name, forecasts)
        self.assertTrue(exists(csv_name))

    def test_or_none_happy(self):
        self.assertEqual(24, or_none("name", lambda x: x + 1, 23))

    def test_or_none_unhappy(self):
        self.assertEqual(None, or_none("name", lambda x: x / 0, 23))

    def fake_spot_check_response(self):
        return {
            "spot": {
                "name": "Blackies",
                "breadcrumb": [
                    {
                        "name": "United States",
                        "href": "https://www.surfline.com/surf-reports-forecasts-cams/united-states/6252001",
                    },
                    {
                        "name": "California",
                        "href": "https://www.surfline.com/surf-reports-forecasts-cams/united-states/california/5332921",
                    },
                    {
                        "name": "Orange County",
                        "href": "https://www.surfline.com/surf-reports-forecasts-cams/united-states/california/orange-county/5379524",
                    },
                    {
                        "name": "Newport Beach",
                        "href": "https://www.surfline.com/surf-reports-forecasts-cams/united-states/california/orange-county/newport-beach/5376890",
                    },
                ],
                "lat": 33.60891872680435,
                "lon": -117.9311192035675,
                "cameras": [
                    {
                        "_id": "582355e11ee905c72145623c",
                        "title": "OC - Blackies",
                        "streamUrl": "https://cams.cdn-surfline.com/cdn-wc/wc-blackies/playlist.m3u8",
                        "stillUrl": "https://camstills.cdn-surfline.com/wc-blackies/latest_small.jpg",
                        "rewindBaseUrl": "https://camrewinds.cdn-surfline.com/wc-blackies/wc-blackies",
                        "isPremium": False,
                        "isPrerecorded": False,
                        "lastPrerecordedClipStartTimeUTC": "2021-10-09T20:55:49.450Z",
                        "lastPrerecordedClipEndTimeUTC": "2021-10-09T20:55:49.450Z",
                        "alias": "wc-blackies",
                        "supportsHighlights": True,
                        "supportsCrowds": False,
                        "status": {
                            "isDown": False,
                            "message": "",
                            "subMessage": "",
                            "altMessage": "",
                        },
                        "control": "https://camstills.cdn-surfline.com/wc-blackies/latest_small.jpg",
                        "nighttime": False,
                        "rewindClip": "https://camrewinds.cdn-surfline.com/wc-blackies/wc-blackies.1300.2021-10-09.mp4",
                    },
                    {
                        "_id": "5a203785096c27001ac4f18c",
                        "title": "OC - Blackies Close-Up",
                        "streamUrl": "https://cams.cdn-surfline.com/cdn-wc/wc-blackiesclose/playlist.m3u8",
                        "stillUrl": "https://camstills.cdn-surfline.com/wc-blackiesclose/latest_small.jpg",
                        "rewindBaseUrl": "https://camrewinds.cdn-surfline.com/wc-blackiesclose/wc-blackiesclose",
                        "isPremium": False,
                        "isPrerecorded": False,
                        "lastPrerecordedClipStartTimeUTC": "2021-10-09T20:55:49.453Z",
                        "lastPrerecordedClipEndTimeUTC": "2021-10-09T20:55:49.453Z",
                        "alias": "wc-blackiesclose",
                        "supportsHighlights": True,
                        "supportsCrowds": False,
                        "status": {
                            "isDown": False,
                            "message": "",
                            "subMessage": "",
                            "altMessage": "",
                        },
                        "control": "https://camstills.cdn-surfline.com/wc-blackiesclose/latest_small.jpg",
                        "nighttime": False,
                        "rewindClip": "https://camrewinds.cdn-surfline.com/wc-blackiesclose/wc-blackiesclose.1300.2021-10-09.mp4",
                    },
                    {
                        "_id": "5cb6590e37ad9fe847480cef",
                        "title": "OC - Newport Pier, Northside",
                        "streamUrl": "https://cams.cdn-surfline.com/cdn-wc/wc-newportpierns/playlist.m3u8",
                        "stillUrl": "https://camstills.cdn-surfline.com/wc-newportpierns/latest_small.jpg",
                        "rewindBaseUrl": "https://camrewinds.cdn-surfline.com/wc-newportpierns/wc-newportpierns",
                        "isPremium": False,
                        "isPrerecorded": False,
                        "lastPrerecordedClipStartTimeUTC": "2021-10-09T20:55:49.452Z",
                        "lastPrerecordedClipEndTimeUTC": "2021-10-09T20:55:49.452Z",
                        "alias": "wc-newportpierns",
                        "supportsHighlights": False,
                        "supportsCrowds": False,
                        "status": {
                            "isDown": False,
                            "message": "",
                            "subMessage": "",
                            "altMessage": "",
                        },
                        "control": "https://camstills.cdn-surfline.com/wc-newportpierns/latest_small.jpg",
                        "nighttime": False,
                        "rewindClip": "https://camrewinds.cdn-surfline.com/wc-newportpierns/wc-newportpierns.1300.2021-10-09.mp4",
                    },
                ],
                "subregion": {
                    "_id": "58581a836630e24c44878fd6",
                    "forecastStatus": "active",
                },
                "abilityLevels": ["BEGINNER", "INTERMEDIATE", "ADVANCED"],
                "boardTypes": [
                    "SHORTBOARD",
                    "FISH",
                    "FUNBOARD",
                    "LONGBOARD",
                    "BODYBOARD",
                ],
                "legacyId": 53412,
                "legacyRegionId": 2143,
                "travelDetails": {
                    "abilityLevels": {
                        "description": "Everyone from total novices to pro longboarders and high-performance shredders.",
                        "levels": ["BEGINNER", "INTERMEDIATE", "ADVANCED"],
                        "summary": "BEGINNER, INTERMEDIATE, ADVANCED",
                    },
                    "best": {
                        "season": {
                            "description": "Autumn typically provides a combination of south and west swells, as well as ideal wind and weather conditions.",
                            "value": ["Autumn", "Winter"],
                        },
                        "tide": {
                            "description": "All tides.",
                            "value": [
                                "Low",
                                "Medium_Low",
                                "Medium",
                                "Medium_High",
                                "High",
                            ],
                        },
                        "size": {
                            "description": "Knee- to head-high.",
                            "value": ["3-8"],
                        },
                        "windDirection": {"description": "NE", "value": []},
                        "swellDirection": {
                            "description": "Short to mid-period WSW/W swells",
                            "value": [],
                        },
                    },
                    "bottom": {
                        "description": "Sand bar fed by a nearby jetty and pier.",
                        "value": ["Sand"],
                    },
                    "crowdFactor": {
                        "description": "This is the heart of Newport Beach's hipster surf culture, so it gets busy.",
                        "rating": 7,
                        "summary": "Moderate",
                    },
                    "localVibe": {
                        "description": "Crowded enough that localism doesn't really matter, although there has definitely been a hierarchy in place for decades.",
                        "rating": 4,
                        "summary": "Doable",
                    },
                    "shoulderBurn": {
                        "description": "You'll deal with a bit of current during long-period swells.",
                        "rating": 5,
                        "summary": "Medium",
                    },
                    "spotRating": {
                        "description": "A regional classic, Blackies is the quintessential Newport beach break.",
                        "rating": 6,
                        "summary": "Fun",
                    },
                    "waterQuality": {
                        "description": "Stays relatively clean as long as there isn't runoff from rainstorms.",
                        "rating": 3,
                        "summary": "Clean",
                    },
                    "travelId": None,
                    "access": "Pay for parking and paddle out between the pier and the jetty.",
                    "breakType": ["Rights", "Lefts", "Beach_Break", "Jetty", "Pier"],
                    "description": "A popular beach break tucked between the 28th Street jetty and the Newport Pier, Blackies has a storied history dating back to the early 1960s, but more recently became the center of the Newport logging scene. Peaky sand bars provide short, fast sections for noseriding when small, while hollow corners serve up barrels and bangable sections when the swell fills in.",
                    "hazards": "Crowds, leashless longboards, rocks, pier supports.",
                    "relatedArticleId": None,
                    "status": "PUBLISHED",
                    "boardTypes": [
                        "SHORTBOARD",
                        "FISH",
                        "FUNBOARD",
                        "LONGBOARD",
                        "BODYBOARD",
                    ],
                },
            },
            "report": {
                "timestamp": 1633892448,
                "forecaster": {
                    "name": "Mike Dippel",
                    "iconUrl": "https://www.gravatar.com/avatar/57d8f3fe8fe5163a2124fd0414d4a5fe?d=mm",
                    "title": "Surf Reporter",
                },
                "body": '<p><strong>Ocean access is closed from Bolsa Chica/Huntington Beach south through the Dana Point Harbor due to a major</strong> <a href="https://www.surfline.com/surf-news/massive-oil-spill-slams-orange-county-beaches/133227" rel="noopener noreferrer" target="_blank"><strong>oil spill</strong></a> <strong>off the coast. If you’re interested in volunteering for upcoming clean-up opportunities, please text ‘oilspill’ (one word) to 51555 or complete&nbsp;</strong><a href="https://app.mobilecause.com/form/lgzoXg?vid=m46kf" rel="noopener noreferrer" target="_blank"><strong>this form</strong></a><strong>.<br>\n<br>\n</strong>&nbsp;</p>\n<p><strong>North OC PM Report</strong>: Conditions have remained clean early this afternoon, however the big 5.9\' high tide at 12:01PM has slowed things down a bit, but spots with good inside bars and reefs are still handling the tide pretty well. New SSW swell continues to fill in with top summer spots seeing chest to shoulder high + sets. Tide drops all afternoon into the evening.&nbsp;</p>\n<p><strong>Rest of Day Outlook</strong>: New long period SSW swell continues to fill in further through the afternoon. Top S swell magnets are seeing chest to shoulder surf, with head high sets expected into the later afternoon. Onshore W wind is expected to pick up over the next few hours, which will put a bump on the surf and worsen conditions. There is a -0.1\' low tide at 7:32PM this evening. Wind may lighten up towards sunset.&nbsp;&nbsp;</p>\n<p><br>\n<strong>NOTE: The Health Department advises against ocean contact within 72 hours of rainfall due to elevated bacteria levels, especially around concentrated areas of runoff like storm drains, creeks and river mouths.</strong></p>',
            },
            "forecast": {
                "note": None,
                "conditions": {
                    "human": True,
                    "value": "NONE",
                    "expired": False,
                    "sortableCondition": 29,
                },
                "wind": {"speed": 6, "direction": 252.95666},
                "waveHeight": {
                    "human": True,
                    "min": 0.5,
                    "max": 1,
                    "occasional": None,
                    "humanRelation": "Shin to knee high",
                    "plus": False,
                },
                "tide": {
                    "previous": {
                        "type": "HIGH",
                        "height": 5.8,
                        "timestamp": 1633892412,
                        "utcOffset": -7,
                    },
                    "current": {
                        "type": "NORMAL",
                        "height": 4.9,
                        "timestamp": 1633899348,
                        "utcOffset": -7,
                    },
                    "next": {
                        "type": "LOW",
                        "height": 0,
                        "timestamp": 1633920095,
                        "utcOffset": -7,
                    },
                },
                "waterTemp": {"min": 62, "max": 63},
                "weather": {"temperature": 70, "condition": "CLEAR"},
                "swells": [
                    {
                        "height": 1.3,
                        "period": 5,
                        "direction": 273.5434,
                        "directionMin": 266.80191,
                        "index": 0,
                    },
                    {
                        "height": 1.2,
                        "period": 13,
                        "direction": 181.63495,
                        "directionMin": 173.626505,
                        "index": 1,
                    },
                    {
                        "height": 1.1,
                        "period": 20,
                        "direction": 198.76959,
                        "directionMin": 195.717255,
                        "index": 2,
                    },
                    {
                        "height": 0.3,
                        "period": 13,
                        "direction": 278.28595,
                        "directionMin": 274.89282000000003,
                        "index": 3,
                    },
                    {
                        "height": 0.2,
                        "period": 20,
                        "direction": 232.71649,
                        "directionMin": 229.52262,
                        "index": 4,
                    },
                    {
                        "height": 0,
                        "period": 0,
                        "direction": 0,
                        "directionMin": 0,
                        "index": 5,
                    },
                ],
            },
        }

    def tearDown(self) -> None:
        if exists(self.TMP_CSV_NAME):
            os.remove(self.TMP_CSV_NAME)

        return super().tearDown()
