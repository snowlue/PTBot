import requests
from bs4 import BeautifulSoup as bs

headers_gadgets, descs_gadgets, originals_gadgets = [], [], []
headers_internet, descs_internet, originals_internet = [], [], []
headers_games, descs_games, originals_games = [], [], []


def refresh_gadgets():
    try:
        global headers_gadgets, descs_gadgets, originals_gadgets
        soup = bs(requests.get('https://news.yandex.ru/gadgets.rss').text, 'html.parser')
        headers_gadgets = [i.contents[0] for i in soup.find_all('title')][2:10]
        originals_gadgets = [i.contents[0] for i in soup.find_all('guid')][:8]
        descs_gadgets = [i.contents[0] for i in soup.find_all('description')][1:9]
    except Exception:
        print('Новости гаджетов не обновлены!')


def refresh_internet():
    try:
        global headers_internet, descs_internet, originals_internet
        soup = bs(requests.get('https://news.yandex.ru/internet.rss').text, 'html.parser')
        headers_internet = [i.contents[0] for i in soup.find_all('title')][2:10]
        originals_internet = [i.contents[0] for i in soup.find_all('guid')][:8]
        descs_internet = [i.contents[0] for i in soup.find_all('description')][1:9]
    except Exception:
        print('Новости интернета не обновлены!')


def refresh_games():
    try:
        global headers_games, descs_games, originals_games
        soup = bs(requests.get('https://news.yandex.ru/games.rss').text, 'html.parser')
        headers_games = [i.contents[0] for i in soup.find_all('title')][2:10]
        originals_games = [i.contents[0] for i in soup.find_all('guid')][:8]
        descs_games = [i.contents[0] for i in soup.find_all('description')][1:9]
    except Exception:
        print('Новости игр не обновлены!')


refresh_games()
refresh_gadgets()
refresh_internet()

print('news.py started!')
