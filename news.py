import time

import requests
from bs4 import BeautifulSoup as bs

headers_gadgets, descs_gadgets, originals_gadgets = [], [], []
headers_internet, descs_internet, originals_internet = [], [], []
headers_games, descs_games, originals_games = [], [], []


def refresh_gadgets():
    try:
        global headers_gadgets, descs_gadgets, originals_gadgets
        headers_gadgets, descs_gadgets, originals_gadgets = [], [], []
        soup = bs(requests.get('https://yandex.ru/news/rubric/gadgets').text, 'html.parser')
        while not soup.find(class_='page-content'):
            soup = bs(requests.get('https://yandex.ru/news/rubric/gadgets').text, 'html.parser')
        code_headers = soup.find_all(class_='link link_theme_black i-bem')

        for i in range(0, 8):
            headers_gadgets.append(code_headers[i].contents[0])
            article_soup = bs(requests.get('https://yandex.ru' + code_headers[i].get('href')).text, 'html.parser')
            while not article_soup.find(class_='doc__text') or not article_soup.find(class_='doc__content'):
                article_soup = bs(requests.get('https://yandex.ru' + code_headers[i].get('href')).text, 'html.parser')
            descs_gadgets.append(article_soup.find(class_='doc__text').contents[0])
            originals_gadgets.append(article_soup.find(class_='doc__content').find('a').get('href'))
    except Exception:
        print('Новости гаджетов не обновлены!')


def refresh_internet():
    try:
        global headers_internet, descs_internet, originals_internet
        headers_internet, descs_internet, originals_internet = [], [], []
        soup = bs(requests.get('https://yandex.ru/news/rubric/internet').text, 'html.parser')
        while not soup.find(class_='page-content'):
            soup = bs(requests.get('https://yandex.ru/news/rubric/internet').text, 'html.parser')
        code_headers = soup.find_all(class_='link link_theme_black i-bem')

        for i in range(0, 8):
            headers_internet.append(code_headers[i].contents[0])
            article_soup = bs(requests.get('https://yandex.ru' + code_headers[i].get('href')).text, 'html.parser')
            while not article_soup.find(class_='doc__text') or not article_soup.find(class_='doc__content'):
                article_soup = bs(requests.get('https://yandex.ru' + code_headers[i].get('href')).text, 'html.parser')
            descs_internet.append(article_soup.find(class_='doc__text').contents[0])
            originals_internet.append(article_soup.find(class_='doc__content').find('a').get('href'))
    except Exception:
        print('Новости интернета не обновлены!')


def refresh_games():
    try:
        global headers_games, descs_games, originals_games
        headers_games, descs_games, originals_games = [], [], []
        soup = bs(requests.get('https://yandex.ru/news/rubric/games').text, 'html.parser')
        while not soup.find(class_='page-content'):
            soup = bs(requests.get('https://yandex.ru/news/rubric/games').text, 'html.parser')
        code_headers = soup.find_all(class_='link link_theme_black i-bem')
        if not code_headers:
            code_headers = soup.find_all(class_='link link_theme_black i-bem link_js_inited')

        for i in range(0, 8):
            headers_games.append(code_headers[i].contents[0])
            article_soup = bs(requests.get('https://yandex.ru' + code_headers[i].get('href')).text, 'html.parser')
            try:
                descs_games.append(article_soup.find(class_='doc__content').find('div').contents[0])
            except:
                descs_games.append(article_soup.find(class_='news-story__content').find('span').contents[0])
            try:
                originals_games.append(article_soup.find(class_='doc__content').find('a').get('href'))
            except:
                originals_games.append(article_soup.find(class_='news-story__content').find('a').get('href'))
    except Exception:
        print('Новости игр не обновлены!')


refresh_games()
refresh_gadgets()
refresh_internet()
print('news.py started!')
