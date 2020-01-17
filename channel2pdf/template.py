from bs4 import BeautifulSoup
import readee

def fact():
	return BeautifulSoup("<div></div>", features="lxml")

def getArticleHtml(name, link, index_loc):
	soup = readee.export(link)
	if len(soup.text) < 100:
		return
	return '''
<html>
	<body>
		<title>%s</title>
		<h1>%s</h1>
		<div><a href="%s">返回目录</a></div>
		%s
		<div><br/><a href="%s">原文</a></div>
		<div><br/><a href="%s">返回目录</a></div>
	</body>
</html>
	''' % (name, name, index_loc, str(soup), link, index_loc)