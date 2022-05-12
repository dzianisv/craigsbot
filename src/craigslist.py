#import get to call a get request on the site
from requests import get
from dataclasses import dataclass
from datetime import datetime
import time
import sys

@dataclass
class Post:
    title: str
    price: float
    link: str
    datetime: datetime

def process_post(post) -> Post:
    _datetime = post.find('time', class_= 'result-date')['datetime']
    # [1:] strips  $ char
    price_str = post.a.text.strip()[1:].replace(',', '')
    price = float(price_str) if len(price_str) != 0 else 0.0
    title = post.find('a', class_='result-title hdrlnk').text
    link = post.find('a', class_='result-title hdrlnk')['href']
    datetime_str = post.find('time', class_= 'result-date')['datetime']
    ad_t = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    return Post(title, price, link, ad_t)


def fetch(url: str):
    #get the first page of the east bay housing prices
    response = get(url) #get rid of those lame-o's that post a housing option without a pic using their filter

    from bs4 import BeautifulSoup
    html_soup = BeautifulSoup(response.text, 'html.parser')

    #get the macro-container for the housing posts
    posts = html_soup.find_all('li', class_= 'result-row')

    for xml in posts:
        post = process_post(xml)
        yield post

if __name__ == "__main__":
    fetch(sys.argv[1])
