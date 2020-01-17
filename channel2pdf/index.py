from datetime import date
from bs4 import BeautifulSoup

def cleanName(name):
    return name.replace('#', '')

def isCN(title):
    if re.search(u'[\u4e00-\u9fff]', title):
        return True
    return False

def getIndexHtml(name, source, links):
	today = date.today().strftime("%m%d")

	index_html = '''
<html>
   <body>
     <h1>%s %s</h1>
     <br/>
     <p style="text-indent:0pt">
     </p>
     <br/>
     <br/>
     <p style="text-indent:0pt">
     	来源：
     	<a href="https://t.me/%s">%s</a>
     </p>
   </body>
</html>
	''' % (name, today, source, name)

	soup = BeautifulSoup(index_html, 'html.parser')
	content_list = soup.find('p')
    titles = []
	for _, title in links.items():
        if isCN(title):
            titles.insert(0, title)
        else:
            titles.append(title)
    for title in titles
		item = '<a href="%s.html">%s</a>' % (cleanName(title), cleanName(title))
		content_list.append(BeautifulSoup(item, 'html.parser'))
		content_list.append(BeautifulSoup('<br/><br/>', 'html.parser'))
	return str(soup)