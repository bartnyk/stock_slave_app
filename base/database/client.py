from pymongo import MongoClient

from base import cfg

client: MongoClient = MongoClient(cfg.MONGODB_URI)
