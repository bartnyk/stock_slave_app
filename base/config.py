from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings

from base.logger import Logger


class Config(BaseSettings):
    # Authentication
    USERNAME: str
    PASSWORD: str

    # App
    SECRET_KEY: str
    DEBUG: bool

    # MongoDB
    MONGODB_HOST: str
    MONGODB_PORT: int
    MONGODB_USERNAME: Optional[str]
    MONGODB_PASSWORD: Optional[str]
    MONGODB_STOCK_DB_NAME: str

    # Email settings
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str
    EMAIL_HOST_PORT: int
    SMTP_SERVER: str
    IMAP_SERVER: str
    POP3_SERVER: str

    # Email recipients
    EMAIL_RECIPIENT: str

    # Urls
    STOCK_RECOMMENDATIONS_URL: str

    # Admin
    ADMIN_EMAIL: str
    ADMIN_PHONE: str

    _root_dir_path: Path = Path(__file__).parent.parent
    _logs_dir_path: Path = _root_dir_path / "logs"
    _logger: Logger = Logger(_logs_dir_path)

    @property
    def email(self) -> dict:
        return {
            "mail": self.EMAIL_HOST_USER,
            "password": self.EMAIL_HOST_PASSWORD,
            "smtp": self.SMTP_SERVER,
            "pop3": self.POP3_SERVER,
            "imap": self.IMAP_SERVER,
            "port": self.EMAIL_HOST_PORT,
        }

    @property
    def logger(self) -> Logger:
        return self._logger

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
