import os
import unittest

from surfsup.excepts import UserInfoNotFoundException
from surfsup.login_info import LoginInfo


class TestLoginInfo(unittest.TestCase):

    def test_not_found(self):
        if os.getenv("USERNAME") != None:
            os.environ.pop("USERNAME")

        if os.getenv("PASSWORD") != None:
            os.environ.pop("PASSWORD")

        with self.assertRaises(UserInfoNotFoundException):
            LoginInfo()

    def test_initialize(self):
        test_username:str = "dummy_username"
        test_password:str = "dummy_password"

        os.environ["USERNAME"] = test_username
        os.environ["PASSWORD"] = test_password

        login = LoginInfo()

        self.assertEqual(login.username, test_username)
        self.assertEqual(login.password, test_password)



if __name__ == '__main__':
    unittest.main()
