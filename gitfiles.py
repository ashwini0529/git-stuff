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

	#Information about a particular repository...
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
	#more features to be added...


def infoAboutUser():
	user = raw_input('Enter the user name of the person you want to see : ')
	url = 'https://github.com/'+user
	def profileInfo():
		soup = BeautifulSoup(urllib2.urlopen(url).read())
		h1 = soup.find('h1', 'vcard-names')
		spans = h1.find_all('span', attrs = {'class': "vcard-fullname"})
		for span in spans:
			print 'Full Name : '+span.string
		spans = h1.find_all('span', attrs = {'class': "vcard-username"})
		for span in spans:
			print 'User Name : '+span.string
		stats = soup.find('div', {'class': 'vcard-stats'}).get_text()
		print stats
	def contributions():
		soup = BeautifulSoup(urllib2.urlopen(url).read())
		totalContributions = soup.find('div' , {'class' : 'contrib-column contrib-column-first table-column'}).get_text()
		print totalContributions
		longestStreak = soup.find('div' , {'class' : 'contrib-column table-column'}).get_text()
		print longestStreak	
		h3 = soup.find('h3', 'conversation-list-heading')
		spans = h3.find_all('span', attrs = {'class': "text-emphasized"})
		for span in spans:
			print 'Total commits this week : '+ span.string
	def popularRepos():
		soup = BeautifulSoup(urllib2.urlopen(url).read())
		popularRepo = soup.find('div' , {'class': 'boxed-group flush'})
		spans = popularRepo.find_all('span', attrs = {'class' : 'repo'})
		countPopularRepo =0
		for span in spans:
			countPopularRepo = countPopularRepo+1
			print str(countPopularRepo)+' : '+span.string
		
	profileInfo()
	contributions()		
	popularRepos()
mainPage()	