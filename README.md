This Telegram Bot allows to keep track of new craigslist.com listings. I use it when need to buy something on the secondary market.
It can be easially self-hosted on Raspberry Pi or other single board computers

# Installation

```sh
apt install -yq python3 pipenv
pipenv sync
```

# Services
|Service|Descrition|
|---|---|
|bin/poller|Polls data from craigslist and notify subscribers about a new ad|
|bin/bot|Telegram bot UX. Listens for the user commands, subscribes, unsubscribes, lists subscriptions|

## Manual testing of craigslist module
```sh
pipenv run python src/crawler.py "https://sfbay.craigslist.org/search/sss?s=120&query=pixel"
```