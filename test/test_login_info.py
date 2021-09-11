import os
import unittest

from surfsup.excepts import UserInfoNotFoundException
from surfsup.login_info import LoginInfo


class TestLoginInfo(unittest.TestCase):
    env_username:str = "SURFLINE_USERNAME"
    env_password:str = "SURFLINE_PASSWORD"


    def test_not_found(self) -> None:
        if os.getenv(self.env_username) != None:
            os.environ.pop(self.env_username)

        if os.getenv(self.env_password) != None:
            os.environ.pop(self.env_password)

        with self.assertRaises(UserInfoNotFoundException):
            LoginInfo()


    def test_initialize(self) -> None:
        fake_username:str = "foo"
        fake_password:str = "foobar"
        os.environ[self.env_username] = fake_username
        os.environ[self.env_password] = fake_password

        login = LoginInfo()

        self.assertEqual(login.username, fake_username)
        self.assertEqual(login.password, fake_password)


if __name__ == '__main__':
    unittest.main()
