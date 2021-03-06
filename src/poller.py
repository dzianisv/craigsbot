#!/usr/bin/env python3

import logging
import craigslist
from data import tg, db

def notify(subscriber, post):
    tg.send_message(chat_id=subscriber['telegram_chat_id'], text=f"${post.price}\n{post.link}")

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
