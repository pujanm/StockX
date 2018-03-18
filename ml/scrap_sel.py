from bs4 import BeautifulSoup, SoupStrainer
import urllib3
import re

opener = urllib3.build_opener()

url = 'http://www.bbc.co.uk/news'
soup = BeautifulSoup(opener.open(url), "lxml")

titleTag = soup.html.head.title

print(titleTag.string)

titles = soup.find_all('span', {'class' : 'title-link__title-text'})

headlines = [t.text for t in titles]

print(headlines)