import json, datetime, re
from .core import Core
import urllib, socket
from bs4 import BeautifulSoup

class BBC(Core):
    
    def __init__(self, format = "json"):
        super().__init__()
        self.html = ''
        return
    
    def getDate(self, item):
        return datetime.datetime.strptime(item['pubDate'][5:16], '%d %b %Y')
    
    def getContent(self, item):
        content = self.getPageContent(item['link'])
        if not content:
            return '';
        return item['title'] + '. ' + content
    
    def getTitle(self, item):
        return item['title']
    

    def getShortDescription(self, item):
        return item['description']
    
    def fetchPage(self, link):
        try:
            fp = urllib.request.urlopen(link, timeout = self.timeout)
            mybytes = fp.read()
            page = mybytes.decode("utf8")
            fp.close()
        except socket.timeout as e:
            print(type(e))
            print(link)
            print("There was an error: %r" % e)
            return None  
        except urllib.error.HTTPError as e:
            print(type(e))
            print(link)
            print("There was an error: %r" % e)
            return None
        except urllib.error.URLError as e:
            print(type(e))
            print(link)
            print("There was an error: %r" % e)
            return None 
        
        self.html = ''
        soup = BeautifulSoup(page, features="html.parser")
        title = soup.find('title');
        description = soup.find("meta", {"name": "description"}).attrs['content']
        date = soup.find('time');
        item = {
            'title': re.sub(' - BBC News$', '', title.text),
            'description': description,
            'pubDate': date.get('datetime'),
            'link': link,
            'content': self.getPageContent(soup),
            'content_html': self.html
        }
        return item
    
    
    def getPageContent(self, soup):
        divs = soup.findAll('div', attrs={"class":"story-body__inner"})
        if divs:
            return self.getDivText(divs)
 
        text = ''
        articles = soup.findAll('article')
        for article in articles:
            for item in article.findChildren():
                if not self.shouldIncludeItem(item):
                    continue
                if item.name in ['div']:
                    text += self.getDivText(item.findChildren())
                elif item.name in ['p', 'ul', 'li', 'ol', 'h2', 'h3']:
                    value = str(item.text)
                    text += value + ' '
                    if value:
                        self.html += '<' + item.name + '>' + value + '</' + item.name + '>'
        return text
    
    def shouldIncludeItem(self, item):
        if item.name not in ['p', 'ul', 'li', 'ol', 'div', 'h2', 'h3']:
            return False
        
        if item.attrs and 'class' in item.attrs.keys():
            for cssClass in item.attrs['class']:
                if cssClass.find('RichText') != -1:
                    return True
        
        return False
        
    
    def getDivText(self, divs):
        text = '';
        for div in divs:
            for item in div.findChildren():
                if item.name in ['p', 'ul', 'li', 'ol', 'h2', 'h3']:
                    value = str(item.text)
                    text += value + ' '
                    if value:
                        self.html += '<' + item.name + '>' + value + '</' + item.name + '>'
        return text

    