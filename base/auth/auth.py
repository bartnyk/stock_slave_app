from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username: str) -> None:
        self.username = username

    def get_id(self, *args, **kwargs) -> str:
        return self.username
