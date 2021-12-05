from os import read
import unittest

from surfsup.comm.message_builder import MessageBuilder

class TestMessageBuilder(unittest.TestCase):

    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self.messenger = MessageBuilder()

    def test_apostrophe_spot(self):
        spot = "Swami's?"   # apostrophe (U+0027)
        self.messenger.is_spot(spot)

    def test_grave_accent(self):
        spot = "Swami`s?"    # grave accent (U+0060)
        self.messenger.is_spot(spot)

    def test_open_single_quoatation(self):
        spot = "Swami‘s?"    # left single quotation mark (U+2018)
        self.messenger.is_spot(spot)

    def test_close_single_quotation(self):
        spot = "Swami’s?"    # right single quotation mark (U+2019)
        self.messenger.is_spot(spot)
