import os
import feedparser
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup

import requests
from lxml import html
'''
def encodeUrl( url ):
    #this func encode HEB to be able to usr as url
    url = list(urllib.parse.urlsplit(url))
    url[2] = urllib.parse.quote(url[2])
    url = urllib.parse.urlunsplit(url)
    return url


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.69 Safari/537.36"

windows_forbidden_chars = ['<','>',':',"/","\\","|","?",'*',' ']

d = feedparser.parse('https://www.moridim.tv/rss')

#for entri in d['entries']:
entri = d['entries'][0]
print(entri['title'])
entri['title'] = entri['title'].split('|')[1][1:]
for char in windows_forbidden_chars:
    entri['title'] = entri['title'].replace(char, '_')

#print (entri['published'].split('GMT')[0])
datetime_object = datetime.strptime(entri['published'].split('GMT')[0], '%a, %d %b %Y %H:%M:%S ')
#print (datetime_object)

#filename = "C:\\images\\ "+ entri['title'] + ".jpg"
#print(filename)
#os.makedirs(os.path.dirname(filename), exist_ok=True)
#urllib._urlopener = AppURLopener()
#urllib._urlopener.retrieve(entri['links'][0]['href'], filename)

print(entri['link'])
print(encodeUrl(entri['link']))

req = urllib.request.Request(encodeUrl(entri['link']), headers={'User-Agent': 'Mozilla/5.0'})
moviePage = urllib.request.urlopen(req).read()
bsObj = BeautifulSoup(moviePage)
for li in bsObj.find_all("li",{"id":"release-2"}):
    print(li.get_text())
'''


session_requests = requests.session()

login_url = "https://www.nitrobit.net/login"
result = session_requests.get(login_url)

tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='token']/@value")))[0]
payload = {
    "email": " ",
    "password": " ",
    "login": "",
    "token": authenticity_token
}
result = session_requests.post(login_url, data = payload, headers = dict(referer = login_url))

URL = "http://www.nitrobit.net/view/1AF23E766AC40FA"
result = session_requests.get(URL, headers = dict(referer = URL))
bsObj = BeautifulSoup(result.content)
#print(bsObj.get_text)
for li in bsObj.find_all("a",{"id":"download"}):
    print(li['href'])