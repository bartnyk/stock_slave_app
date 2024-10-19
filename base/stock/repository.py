from base import cfg
from base.database.repository import BaseRepository
from base.stock.schemas import StockRecommendation


class StockRepository(BaseRepository):
    _db_name = cfg.MONGODB_STOCK_DB_NAME

    def get_recommendations(self) -> list:
        recommendations: list = self.get_all({})
        recommendations = [StockRecommendation(**rec) for rec in recommendations]
