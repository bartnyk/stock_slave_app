from urllib.parse import quote_plus

from pymongo import MongoClient

from base import cfg


class Mongo:
    @staticmethod
    def create_client(uri: str) -> MongoClient:
        return MongoClient(uri)

    @staticmethod
    def create_uri(database_name: str) -> str:
        if cfg.MONGODB_USERNAME and cfg.MONGODB_PASSWORD:
            username = quote_plus(cfg.MONGODB_USERNAME)
            password = quote_plus(cfg.MONGODB_PASSWORD)

            return f"mongodb://{username}:{password}@{cfg.MONGODB_HOST}:{cfg.MONGODB_PORT}/{database_name}"

        return f"mongodb://{cfg.MONGODB_HOST}:{cfg.MONGODB_PORT}/{database_name}"
