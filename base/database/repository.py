from abc import ABC

from pymongo.database import Collection, Database

from base.database.client import client


class BaseRepository(ABC):
    _db_name: str

    def __init__(self, collection: str) -> None:
        self._db: Database = client.get_database(self._db_name)
        self._collection_name: str = collection

    @property
    def collection(self) -> Collection:
        return self._db[self._collection_name]

    def get(self, query: dict) -> dict:
        return self.collection.find_one(query)

    def get_all(self, query: dict = {}) -> list:
        return list(self.collection.find(query))

    def insert(self, data: dict) -> None:
        self.collection.insert_one(data)
