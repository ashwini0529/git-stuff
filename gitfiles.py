import urllib2
from bs4 import BeautifulSoup
import requests

def mainPage():
	print '''Welcome to the Python Interface of GitHub!
	Please enter your choice : 
	1. Get information about user
	2. Get information about a particular repository\n'''
	choice = int(raw_input('Enter your choice here: '))
	if(choice == 1):
		infoAboutUser()
	elif (choice == 2):
		infoAboutRepo()
def infoAboutRepo():
	user = raw_input('Enter the user name ')
	repo = raw_input('Enter the repository name : ')
	def pulse():
		url = "https://github.com/"+user+'/'+repo+'/pulse/monthly'
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
	#watching not working as of now. Only giving 0 as Watcher...
	def watching():
		url = "https://github.com/"+user+'/'+repo
		soup = BeautifulSoup(urllib2.urlopen(url).read())
		watch = soup.find('a' , {"class" : "social-count js-social-count"}).get_text()
		print 'Watchers: ' + watch
	pulse()
	readme()
	watching()
mainPage()