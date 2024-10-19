from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Authentication
    USERNAME: str
    PASSWORD: str

    # App
    SECRET_KEY: str
    DEBUG: bool

    # MongoDB
    MONGODB_URI: str
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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
