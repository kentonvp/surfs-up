from os import getenv
from surfsup.excepts import UserInfoNotFoundException

class LoginInfo:

    def __init__(self):
        """Initialize user information from environment variables."""
        if getenv("USERNAME") == None or getenv("PASSWORD") == None:
            raise UserInfoNotFoundException

        self.username:str = str(getenv("USERNAME"))
        self.password:str = str(getenv("PASSWORD"))

