import urllib2
from bs4 import BeautifulSoup
import requests
user = raw_input('Enter the user name ')
repo = raw_input('Enter the repository name : ')
def pulse():
	url = "https://github.com/"+user+'/'+repo+'/pulse'
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	print '''
	The whole information about the repository is as follows :\name'''
	for each_div in soup.findAll('div',{'class':'section diffstat-summary'}):
	    print each_div.get_text()
def readme():
	url = "https://github.com/"+user+'/'+repo+'/blob/master/README.md'
	soup = BeautifulSoup(urllib2.urlopen(url).read())
	paragraphs = soup.find('article', {"class" : "markdown-body entry-content"}).get_text()
	print '''README\n'''
	print paragraphs
	
pulse()
readme()