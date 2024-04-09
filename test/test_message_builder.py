import unittest
from unittest.mock import patch

from surfsup.comm.message_builder import MessageBuilder


class TestMessageBuilder(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self.messenger = MessageBuilder()

    def test_is_spot(self):
        self.assertTrue(self.messenger.is_spot("Swami's"))
        self.assertTrue(self.messenger.is_spot("Blacks"))
        self.assertFalse(self.messenger.is_spot("SMLKJDF"))

    def test_clean(self):
        ex_obj = {
            "conditions": {"value": "FAIR"},
            "waveHeight": {
                "min": 1,
                "max": 4,
                "humanRelation": "shoulder to head high",
            },
        }
        self.assertEqual(
            "Surf Report: 😐 FAIR\nSurf is 1ft to 4ft, shoulder to head high.\nHave fun!",
            self.messenger.clean(ex_obj),
        )

    def test_build_report_message_bad(self):
        msg = self.messenger.build_report_message("Blcks")
        self.assertEqual(
            "ERROR: Blcks was invalid. Possible corrections:\nBlacks\nDid you need /help?",
            msg,
        )

    def test_build_report_message_good(self):
        ex_obj = {
            "conditions": {"value": "FAIR"},
            "waveHeight": {
                "min": 1,
                "max": 4,
                "humanRelation": "shoulder to head high",
            },
        }
        with patch("surfsup.surfline.api.SurflineAPI.spot_check") as mock_spot_check:
            mock_spot_check.return_value = {"forecast": ex_obj}
            msg = self.messenger.build_report_message("Blacks")
            self.assertEqual(
                "Surf Report: 😐 FAIR\nSurf is 1ft to 4ft, shoulder to head high.\nHave fun!",
                msg,
            )

    def test_build_report_message_apostrophes(self):
        ex_obj = {
            "conditions": {"value": "FAIR"},
            "waveHeight": {
                "min": 1,
                "max": 4,
                "humanRelation": "shoulder to head high",
            },
        }
        with patch("surfsup.surfline.api.SurflineAPI.spot_check") as mock_spot_check:
            mock_spot_check.return_value = {"forecast": ex_obj}
            msg = self.messenger.build_report_message("Swami's")
            self.assertEqual(
                "Surf Report: 😐 FAIR\nSurf is 1ft to 4ft, shoulder to head high.\nHave fun!",
                msg,
            )
