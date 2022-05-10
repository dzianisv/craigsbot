#import get to call a get request on the site
from requests import get
from dataclasses import dataclass
import sys

@dataclass
class Post:
    title: str
    price: float
    link: str


def process_post(post) -> Post:
    _datetime = post.find('time', class_= 'result-date')['datetime']
    # [1:] strips  $ char
    price = post.a.text.strip()[1:].replace(',', '')
    title = post.find('a', class_='result-title hdrlnk').text
    link = post.find('a', class_='result-title hdrlnk')['href']
    return Post(title, price, link)


def crawl(url: str):
    #get the first page of the east bay housing prices
    response = get(url) #get rid of those lame-o's that post a housing option without a pic using their filter

    from bs4 import BeautifulSoup
    html_soup = BeautifulSoup(response.text, 'html.parser')

    #get the macro-container for the housing posts
    posts = html_soup.find_all('li', class_= 'result-row')

    for xml in posts:
        post = process_post(xml)
        print(post)

if __name__ == "__main__":
    crawl(sys.argv[1])
