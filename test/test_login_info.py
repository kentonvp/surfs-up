import os
import unittest

from surfsup.excepts import UserInfoNotFoundException
from surfsup.login_info import LoginInfo


class TestLoginInfo(unittest.TestCase):
    env_username:str = "SURFLINE_USERNAME"
    env_password:str = "SURFLINE_PASSWORD"

    def test_not_found(self):
        if os.getenv(self.env_username) != None:
            os.environ.pop(self.env_username)

        if os.getenv(self.env_password) != None:
            os.environ.pop(self.env_password)

        with self.assertRaises(UserInfoNotFoundException):
            LoginInfo()

    def test_initialize(self):
        os.environ["USERNAME"] = self.env_username
        os.environ["PASSWORD"] = self.env_password

        login = LoginInfo()

        self.assertEqual(login.username, self.env_username)
        self.assertEqual(login.password, self.env_password)


if __name__ == '__main__':
    unittest.main()
