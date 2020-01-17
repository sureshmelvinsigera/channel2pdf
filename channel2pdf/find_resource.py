import os
from bs4 import BeautifulSoup
import yaml
from telegram_util import matchKey
import cached_url
from datetime import date

LINK_PREFIX = 'https://t.me/s/'

def findResource(source):
	soup = BeautifulSoup(cached_url.get(LINK_PREFIX + source), 'html.parser')
	name = soup.find('meta', {'property': 'og:title'})['content']
	links = {}
	for item in soup.find_all('a', class_='tgme_widget_message_link_preview'):
		if 'telegra.ph' not in item['href']:
			continue
		title = item.find('div', class_='link_preview_title').text
		links[item['href']] = title
	pics = []
	for item in soup.find_all('a', class_='tgme_widget_message_photo_wrap'):
		text = item.parent.find('div', class_='tgme_widget_message_text')
		pics.append((item, text))
	texts = []
	for item in soup.find_all('div', class_='tgme_widget_message_wrap'):
		if 'telegra.ph' in item.text:
			continue
		if item.find('a', class_='tgme_widget_message_photo_wrap'):
			continue
		preview = item.find('a', class_='tgme_widget_message_link_preview')
		text = item.find('div', class_='tgme_widget_message_text')
		texts.append((text, preview))
	return name, links, pics, texts

	
