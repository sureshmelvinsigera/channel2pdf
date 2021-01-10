#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import channel2pdf
import os
import sys

def test():
	additional_setting = '--paper-size b6 --pdf-page-margin-left 15 ' + \
		'--pdf-page-margin-right 15 --pdf-page-margin-top 15 ' + \
		'--pdf-page-margin-bottom 15'
	# pdf_name = channel2pdf.gen('mengyshare')
	pdf_name = channel2pdf.gen('social_justice_watch')
	os.system('open %s -g' % pdf_name)
	# channel2pdf.gen('mengyshare', filename_suffix='_大字版', additional_setting=additional_setting)
	# pdf_name = channel2pdf.gen('pincongessence',
	# 	filename_suffix='_大字版', additional_setting=additional_setting)
	# pdf_name = channel2pdf.gen('equality_and_rights')
	# os.system('open %s -g' % pdf_name)
	# pdf_name = channel2pdf.gen('social_justice_watch')
	# os.system('open %s -g' % pdf_name)
	
if __name__=='__main__':
	test()