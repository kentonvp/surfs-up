from os import read
import unittest

from surfsup.comm.message_builder import MessageBuilder

class TestMessageBuilder(unittest.TestCase):

    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self.messenger = MessageBuilder()

    def test_is_spot(self):
        spot = input("Swami's?")
        self.messenger.is_spot(spot)
