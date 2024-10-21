import logging
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


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
    def root_dir(self) -> Path:
        return Path(__file__).parent.parent

    @property
    def logs_dir(self) -> Path:
        path = self.root_dir / "logs"
        path.mkdir(exist_ok=True)
        return path

    @property
    def logger(self) -> logging.Logger:
        logger = logging.getLogger("app")
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(self.logs_dir / "app.log")
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    @property
    def stock_logger(self) -> str:
        file_handler = logging.FileHandler(self.logs_dir / "stock.log")
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        logger = self.logger
        logger.addHandler(file_handler)

        return logger

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
