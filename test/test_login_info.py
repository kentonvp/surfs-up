import os
import unittest

from surfsup.login_info import LoginInfo


class TestLoginInfo(unittest.TestCase):
    def test_initialize(self) -> None:
        fake_username: str = "foo"
        fake_password: str = "foobar"

        login = LoginInfo(fake_username, fake_password)

        self.assertEqual(login.username, fake_username)
        self.assertEqual(login.password, fake_password)
