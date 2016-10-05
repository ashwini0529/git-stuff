"""
Program to find information about given Github username or
repository from the terminal.
"""
import urllib2
from bs4 import BeautifulSoup
import requests


def infoAboutRepo():
	"""
	Given username and repository, Returns information about the repository.
	"""
	user = raw_input('Enter the user name ')
	repo = raw_input('Enter the repository name : ')
	url = "https://github.com/"+user+'/'+repo
	try:
		urllib2.urlopen(url)
	except urllib2.HTTPError, e:
		print 'Sorry, there is no such repository named "%s" for user "%s"'%(repo, user)
		exit()


	def pulse(url):
		"""
		"""
		url+= '/pulse/monthly'
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page.read())
		div_all = soup.findAll('div',{'class':'section diffstat-summary'})
		if not div_all:
			print 'No Recent activities in the repository.'
			return
		print 'The whole information about the repository is as follows :\n'
		for each_div in div_all:
		    print each_div.get_text()

	def readme(url):
		"""
		"""
		url+= '/blob/master/README.md'
		# Check if ReadMe exists.
		try:
			soup = BeautifulSoup(urllib2.urlopen(url).read())
			paragraphs = soup.find('article', {"class" : "markdown-body entry-content"}).get_text()
		except Exception:
			print 'ReadMe file for the repository doesn\'t exist'
			return

		print 'README\n'
		print paragraphs


	def watching(url):
		"""
		"""
		# TODO: watching not working as of now. Only giving 0 as Watcher...
		soup = BeautifulSoup(urllib2.urlopen(url).read())
		watch = soup.find('a' , {"class" : "social-count js-social-count"}).get_text()
		print 'Watchers: %s' %(watch)


	def statistics(url):
		"""
		"""
		soup = BeautifulSoup(urllib2.urlopen(url).read())
		ultags_all= soup.find_all('ul', {'class' : 'numbers-summary'})
		if not ultags_all:
			print 'No activities in the repository.'
			return

		for ultag in ultags_all :
			for litag in ultag.find_all('li'):
				print litag.text

	statistics(url)
	pulse(url)
	readme(url)
	#watching(url) ---> Now not showing correct watch number.. always 0
	#more features to be added...


def infoAboutUser():
	"""
	Given username, Returns information about user if exists.
	"""
	user = raw_input('Enter the user name of the person you want to see : ')
	url = 'https://github.com/'+user
	# Check If username is invalid
	try:
		soup = BeautifulSoup(urllib2.urlopen(url).read())
	except Exception:
		print 'User "%s" does not exist! Please try again.' %(user)
		exit()


	def profileInfo(soup):
		"""
		Returns the Profile specific information for the User.
		"""
		# TODO: remove unwanted code

		#Give users full name
		fullName = soup.find('span', attrs = {'class': "vcard-fullname"}).text
		print "\nFull name: ",fullName
		
		#Give users username
		userName = soup.find('span', attrs = {'class': "vcard-username"}).text
		print "\nusername: ",userName
		
		#Give users home town
		try:
			homeTown = soup.find('li',{'aria-label':"Home location"}).text
			print "\nHome Town: ",homeTown
		except:
			print "\nUser does not add his/her hometown on github!"
		#Give user Email-Id
		try:
			email_id = soup.find('li',{'aria-label' : "Email"}).text
			print "\nemail-id: ",email_id
		except:
			print "\nUser does not add his/her email-id on github!"
			
		#Give Joining date
		join = soup.find('li',{'aria-label':"Member since" }).text
		print "\nJoining date of github: ",join[10:]
		
		#Give users oraginsation 
		try:
			organization = soup.find('li',{'aria-label' : "Organization"}).text
			print "\nOrganization: ",organization
		except:
			print "\nUser does not add his/her working Organization on github!"

		#Give users Blog or Website 
		try:
			website = soup.find('li',{'aria-label' : "Blog or website"}).text
			print "\nPersonal website: ",website
		except:
			print "\nUser does not add his/her personal website on github!\n"
		
	def contributions(soup):
		"""
		Returns the contributions done by user in given Period.
		"""
		# TODO: Generates error. Needs modification
		totalContributions = soup.find('div' , {'class' : 'contrib-column contrib-column-first table-column'}).get_text()
		print totalContributions
		longestStreak = soup.find('div' , {'class' : 'contrib-column table-column'}).get_text()
		print longestStreak	
		h3 = soup.find('h3', 'conversation-list-heading')
		spans = h3.find_all('span', attrs = {'class': "text-emphasized"})
		for span in spans:
			print 'Total commits this week : '+ span.string


	def popularRepos(soup):
		"""
		Returns Public repositories of the user.
		"""
		popularRepo = soup.find('div' , {'class': 'boxed-group flush'})
		spans = popularRepo.find_all('span', attrs = {'class' : 'repo'})
		if not spans:
			print 'No public repositories for the given user.'
			return
		countPopularRepo =0
		for span in spans:
			countPopularRepo = countPopularRepo+1
			print str(countPopularRepo)+' : '+span.string

	profileInfo(soup)
	contributions(soup)
	popularRepos(soup)

if __name__ == "__main__":
	print "Welcome to the Python Interface of GitHub!"
	print '''Please enter your choice :\n
	1. Get information about user
	2. Get information about a particular repository\n'''

	#Small changes here for ask user for his choice
	while True:
		choice = raw_input('Enter your choice here: ')
		if choice == '1':
			infoAboutUser()
			break
		elif choice == '2':
			infoAboutRepo()
			break
		else:
			print "Sorry, It is not a valid choice.Please select from 1 and 2!\n\n"
	
	