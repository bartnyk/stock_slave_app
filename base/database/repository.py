from abc import ABC

from pymongo import MongoClient
from pymongo.database import Collection, Database

from base.database.client import Mongo


class BaseRepository(ABC):
    _db_name: str = ""

    def __init__(self, collection: str) -> None:
        mongodb_uri = Mongo.create_uri(self._db_name)
        self._client: MongoClient = Mongo.create_client(mongodb_uri)
        self._db: Database = self._client.get_database(self._db_name)
        self._collection = self._db[collection]

    @property
    def collection(self) -> Collection:
        return self._collection

    def get(self, query: dict) -> dict:
        return self.collection.find_one(query)

    def get_all(self, query: dict = {}) -> list:
        return list(self.collection.find(query))

    def insert(self, data: dict) -> None:
        self.collection.insert_one(data)
