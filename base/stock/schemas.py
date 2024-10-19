from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, RootModel


class StockRecommendation(BaseModel):
    _id: Optional[ObjectId]
    id: str
    date: str
    time: str
    title: str
    instrument: str
    recommendation: str
    price: str
    target_price: list[str]
    author: str
    commitment_period: str

    @property
    def full_datetime(self) -> str:
        return f"{self.date} -- {self.time}"

    @classmethod
    def get_id(cls, title: str) -> str:
        return title.split("[")[1].split("]")[0]


class StockRecommendationList(RootModel):
    root: list[StockRecommendation] = []
    _titles: set = set()

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    @classmethod
    def parse(cls, data: list[dict]) -> "StockRecommendationList":
        instance = cls()
        instance.root = [StockRecommendation(**rec) for rec in data]
        return instance

    def is_recommendation_exists(self, title: str) -> bool:
        if not self._titles:
            self._titles = {rec.title for rec in self.root}
        return title in self._titles

    def last(self) -> StockRecommendation:
        return self.root[0]

    def append(self, recommendation: StockRecommendation) -> None:
        self.root.append(recommendation)
