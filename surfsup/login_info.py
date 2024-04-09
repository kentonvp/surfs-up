class LoginInfo:
    def __init__(self, username: str, password: str):
        """Initialize user information from environment variables."""

        self.username: str = username
        self.password: str = password
