from base import cfg
from base.database.repository import BaseRepository


class StockRepository(BaseRepository):
    _db_name = cfg.MONGODB_STOCK_DB_NAME
