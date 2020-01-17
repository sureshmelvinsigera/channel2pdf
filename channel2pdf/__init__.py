#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'channel2pdf'

import os
from .find_resource import findResource
from .article import getArticleHtml
from .index import getIndexHtml, cleanName
from datetime import date

if os.name == 'posix':
	ebook_convert_app = '/Applications/calibre.app/Contents/MacOS/ebook-convert'
else:
	ebook_convert_app = 'ebook-convert'

def gen(source, ebook_convert_app=ebook_convert_app):
	name, links, pics, texts = findResource(source)
	filename = '%s_%s' % (date.today().strftime("%m%d"), name)

	os.system('rm -rf html_result')	
	os.system('mkdir html_result > /dev/null 2>&1')

	print(links)
	for link, title in links.copy().items():
		html = getArticleHtml(title, link, filename + '.html')
		if html:
			with open('html_result/%s.html' % cleanName(title), 'w') as f:
				f.write(html)
		else:
			del links[link]

	print(links)

	index_html_name = 'html_result/%s.html' % filename
	with open(index_html_name, 'w') as f:
		f.write(getIndexHtml(name, source, links))

	os.system('mkdir pdf_result > /dev/null 2>&1')
	pdf_name = 'pdf_result/%s.pdf' % filename
	os.system('%s %s %s > /dev/null 2>&1' % (ebook_convert_app, index_html_name, pdf_name))
	return pdf_name
		
