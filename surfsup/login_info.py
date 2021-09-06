from os import getenv
from surfsup.excepts import UserInfoNotFoundException

class LoginInfo:

    def __init__(self):
        """Initialize user information from environment variables."""
        env_username:str = "SURFLINE_USERNAME"
        env_password:str = "SURFLINE_PASSWORD"
        if getenv(env_username) == None or getenv(env_password) == None:
            raise UserInfoNotFoundException

        self.username:str = str(getenv(env_username))
        self.password:str = str(getenv(env_password))

