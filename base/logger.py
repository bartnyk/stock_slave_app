import logging
import logging.config
from pathlib import Path


class Logger:
    def __init__(self, dir_path: Path) -> None:
        self._dir_path = dir_path
        self.setup_logging()

    def setup_logging(self) -> None:
        logging.config.dictConfig(self.config)

    @property
    def config(self) -> dict:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "app_file": {
                    "class": "logging.FileHandler",
                    "level": "DEBUG",
                    "formatter": "default",
                    "filename": self._dir_path / "app.log",
                },
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "default",
                },
                "stock_file": {
                    "class": "logging.FileHandler",
                    "level": "DEBUG",
                    "formatter": "default",
                    "filename": self._dir_path / "stock.log",
                },
                "command_file": {
                    "class": "logging.FileHandler",
                    "level": "DEBUG",
                    "formatter": "default",
                    "filename": self._dir_path / "command.log",
                },
            },
            "loggers": {
                "app": {
                    "level": "DEBUG",
                    "handlers": ["app_file", "console"],
                    "propagate": False,
                },
                "app.stock": {
                    "level": "DEBUG",
                    "handlers": ["stock_file", "console"],
                    "propagate": False,
                },
                "app.command": {
                    "level": "DEBUG",
                    "handlers": ["command_file", "console"],
                    "propagate": False,
                },
            },
        }

    @property
    def app(self) -> logging.Logger:
        return logging.getLogger("app")

    @property
    def stock(self) -> logging.Logger:
        return logging.getLogger("app.stock")

    @property
    def command(self) -> logging.Logger:
        return logging.getLogger("app.command")
