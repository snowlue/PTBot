import requests
from bs4 import BeautifulSoup as bs

headers, links, descs, originals = [], [], [], []
site = requests.get('https://m.news.yandex.ru/computers.html')
soup = bs(site.text, 'html.parser')
all_headers = soup.find(class_='page-content').find_all(class_='link link_theme_black i-bem')

for i in range(0, 8):
	links.append('https://m.news.yandex.ru' + all_headers[i].get('href'))
	headers.append(all_headers[i].contents[0])
	

for i in range(0, 8):
	article_site = requests.get(links[i])
	article_soup = bs(article_site.text, 'html.parser')
	descs.append(article_soup.find(class_='doc__text').contents[0])
	originals.append(article_soup.find(class_='doc__content').find('a').get('href'))
