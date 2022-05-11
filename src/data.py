import os
import telegram
from pymongo import MongoClient

class Config(object):
    def __init__(self):
        self.mongo_url = os.environ.get("MONGODB_URL", None)
        self.telegram_token = os.environ.get("TELEGRAM_TOKEN", None)

config = Config()
client = MongoClient(config.mongo_url)
db = client.craigslistcrawler
tg = telegram.Bot(token=config.telegram_token)
