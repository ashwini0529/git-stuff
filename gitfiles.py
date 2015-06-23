import urllib2
from bs4 import BeautifulSoup
import requests
user = raw_input('Enter the user name ')
repo = raw_input('Enter the repository name : ')
url = "https://github.com/"+user+'/'+repo+'/pulse'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
for each_div in soup.findAll('div',{'class':'section diffstat-summary'}):
    print each_div