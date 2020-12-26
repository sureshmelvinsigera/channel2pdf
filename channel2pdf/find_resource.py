import os
from bs4 import BeautifulSoup
import yaml
from telegram_util import matchKey
import cached_url
from datetime import date
import re
import webgram
import plain_db
import export_to_telegraph

last_msg = plain_db.load('last_msg')

LINK_PREFIX = 'https://t.me/s/'

def findSrc(raw):
	pivot1 = "background-image:url('"
	index = raw.find(pivot1)
	raw = raw[index + len(pivot1):]
	pivot2 = "')"
	index = raw.find(pivot2)
	return raw[:index]

def getLink(post):
	if not post.link:
		return
	return tuple([item['href'] for item in 
		soup.find_all('a') if item.get('href')]), post.link

def findLinks(source):
	last_msg_id = last_msg.get(source) or 1
	links = {}
	for msg_id in range(last_msg_id + 1, last_msg_id + 50):
		r = getLink(webgram.getPost(source, msg_id))
		if not r:
			continue
		last_msg.update(source, msg_id)
		links[r[0]] = r[1]
	for msg_id in range(last_msg_id, last_msg_id - 50, -1):
		if len(links) > 10:
			return links
		r = getLink(webgram.getPost(source, msg_id))
		if not r:
			continue
		links[r[0]] = r[1]
	return links


def findResource(source):
	soup = BeautifulSoup(cached_url.get(LINK_PREFIX + source), 'html.parser')
	name = soup.find('meta', {'property': 'og:title'})['content']
	links = {}
	for item in soup.find_all('a', class_='tgme_widget_message_link_preview'):
		if 'telegra.ph' not in item['href']:
			continue
		title = item.find('div', class_='link_preview_title').text
		links[(item['href'],)] = title
	pics = []
	for item in soup.find_all('div', class_='tgme_widget_message_bubble'):
		imgs = []
		for pic in item.find_all('a', class_='tgme_widget_message_photo_wrap'):
			imgs.append('<figure><img src="%s"/></figure>' % findSrc(pic['style']))
		text = item.find('div', class_='tgme_widget_message_text')
		if imgs:
			pics.append((''.join(imgs), text or ''))
	texts = []
	for item in soup.find_all('div', class_='tgme_widget_message_wrap'):
		if item.find('a', class_='tgme_widget_message_photo_wrap'):
			continue
		preview = item.find('a', class_='tgme_widget_message_link_preview')
		if preview:
			preview.name = 'div'
		text = item.find('div', class_='tgme_widget_message_text')
		texts.append((text, preview or ''))
	if len(links) == 0:
		links = findLinks(source)
	return name, links, pics, texts

	
