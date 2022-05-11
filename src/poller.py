#!/usr/bin/env python3
import os
import binascii
import time
import sys
import telegram
import logging
import threading
import json
from pymongo import MongoClient
from . import craigslist

class Config(object):
    def __init__(self):
        self.mongo_url = os.environ.get("MONGODB_URL", None)
        self.telegram_token = os.environ.get("TELEGRAM_TOKEN", None)

config = Config()
client = MongoClient(config.mongo_url)
db = client.craigslistcrawler
tg = telegram.Bot(token=config.telegram_token)

def notify(subscriber, res):
    tg.send_message(chat_id=subscriber['telegram_chat_id'], text="{url} {price} {where}".format(**res))

def poll(subscriber):
    latest = subscriber["latest"]
    url = subscriber["url"]

    for post in craigslist.fetch(url):
        latest = max(post.datetime, latest) 
        if (post.datetime <= subscriber["latest"]):
            break

        notify(subscriber, post)

    db.subscribers.update_one(
        {"_id": subscriber["_id"]},
        {"$set": {'latest': latest}}
    )

def events_loop():
    for subscriber in db.subscribers.find():
        poll(subscriber)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    events_loop()
