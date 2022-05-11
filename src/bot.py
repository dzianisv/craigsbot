#!/usr/bin/env python3
import logging
import telegram.ext
from data import db, config
from datetime import datetime

def start(u, ctx):
    url = u.message.text.split(' ')[1]
    logging.info("subscribing %d: %s", u.message.chat_id, u.message.text.split(' '))
    db.subscribers.insert_one({
        'telegram_chat_id': u.message.chat_id,
        'url': url,
        'latest': datetime.now(),
    })
    u.message.reply_text('Subscribed')

def list(u, ctx):
    urls = [ doc['url'] for doc in db.subscribers.find({'telegram_chat_id': u.message.chat_id }) ]
    u.message.reply_text(f"Subscribed to {urls}")

def stop(u, ctx):
    logging.info("unsubscribing %d", u.message.chat_id)
    db.subscribers.delete_many({
        'telegram_chat_id': u.message.chat_id
    })
    u.message.reply_text('Unsubscribed from all')

def help(u, ctx):
    u.message.reply_text('/start <url>\tget updates on a new ad at <url>\n/stop\tunsubscribe from the all updated\n/list\tlist all the subscribtions\n')


def telegram_events_loop():
    updater = telegram.ext.Updater(token=config.telegram_token, use_context=True)
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('stop', start))
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('list', list))
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('help', help))
    updater.start_polling()
    updater.idle()
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    telegram_events_loop()
