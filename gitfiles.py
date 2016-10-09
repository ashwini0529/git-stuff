"""
Program to find information about given Github username or
repository from the terminal.
"""
import urllib2
from bs4 import BeautifulSoup
import requests
import re

def infoAboutRepo():
	"""
	Given username and repository, Returns information about the repository.
	"""
	user = raw_input('Enter the user name ')
	url = 'https://github.com/'+user
	# Check If username is invalid
	try:
		soup = BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")
	except Exception:
		print 'User "%s" does not exist! Please try again.' %(user)
		exit()

	popularRepo = soup.find_all('span' , {'class': 'repo js-repo'})
	print "These are the some popular repo of user",user
	for repo in popularRepo:
		print repo.string

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
		url += '/pulse/monthly'
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page.read(), "html.parser")
		div_all = soup.findAll('div',{'class':'section diffstat-summary'})
		if not div_all:
			print 'No Recent activities in the repository.'
			return
		print '\nThe whole information about the repository is as follows :\n'
		for each_div in div_all:
		    print ' '.join(each_div.get_text().split())

	def readme(url):
		"""
		"""
		url+= '/blob/master/README.md'
		# Check if ReadMe exists.
		try:
			soup = BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")
			paragraphs = soup.find('article', {"class" : "markdown-body entry-content"}).get_text()
		except Exception:
			print 'ReadMe file for the repository doesn\'t exist'
			return

		print '\nREADME\n'
		print paragraphs


	def watching(url):
		"""
		"""
		# TODO: watching not working as of now. Only giving 0 as Watcher...
		soup = BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")
		watch = soup.find('a' , {"class" : "social-count js-social-count"}).text
		print 'Watchers: %s' %(watch.split()[0])


	def statistics(url):
		"""
		"""
		soup = BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")
		ultags_all= soup.find_all('ul', {'class' : 'numbers-summary'})
		if not ultags_all:
			print 'No activities in the repository.'
			return
		print "\nUsers Activities in Repo"
		for ultag in ultags_all :
			for litag in ultag.find_all('li'):
				if ' '.join(litag.text.split()) != "Fetching contributors":
					print ' '.join(litag.text.split())

	statistics(url)
	pulse(url)
	readme(url)
	watching(url)
	#more features to be added...


def infoAboutUser():
	"""
	Given username, Returns information about user if exists.
	"""
	user = raw_input('Enter the user name of the person you want to see : ')
	url = 'https://github.com/'+user
	# Check If username is invalid
	try:
		soup = BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")
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
		print "Full name: ",fullName

		#Give users username
		userName = soup.find('span', attrs = {'class': "vcard-username"}).text
		print "username: ",userName

		#Give users home town
		try:
			homeTown = soup.find('li',{'aria-label':"Home location"}).text
			print "Home Town: ",homeTown
		except:
			print "User does not add his/her hometown on github!"
		#Give user Email-Id
		try:
			email_id = soup.find('li',{'aria-label' : "Email"}).text
			print "email-id: ",email_id
		except:
			print "User does not add his/her email-id on github!"

		#Give Joining date
		join = soup.find('li',{'aria-label':"Member since" }).text
		print "Joining date of github: ",join[10:]

		#Give users organisation
		try:
			organization = soup.find('li',{'aria-label' : "Organization"}).text
			print "Organization: ",organization
		except:
			print "User does not add his/her working Organization on github!"

		#Give users Blog or Website
		try:
			website = soup.find('li',{'aria-label' : "Blog or website"}).text
			print "Personal website: ",website
		except:
			print "User does not add his/her personal website on github!"

        # Get followers
		for followersCount in soup.findAll('span', attrs = {'class': "counter"}):
		    parent = followersCount.parent
		    if parent.name == 'a' and 'followers' in parent['href']:
		    	count = followersCount.text.replace(" ",'').replace("\n", "")
			#count = int(re.search(r'\d+', str(followersCount.text)).group())
			print "Followers: ",count
			count = int(re.search(r'\d+', str(followersCount.text)).group())
			if (count > 0):
				follow(url,'followers')

		for followingCount in soup.findAll('span', attrs = {'class': "counter"}):
		    parent = followingCount.parent
		    if parent.name == 'a' and 'following' in parent['href']:
		    	count = followersCount.text.replace(" ", '').replace("\n", "")
			print "Following: ", count
			count = int(re.search(r'\d+', str(followingCount.text)).group())
			if (count > 0):
				follow(url,'following')

		#Give user bio
		try:
			userBio = soup.find('div', attrs = {'class': 'user-profile-bio'}).text
			print "Bio: ",userBio
		except:
			print "User does not add his/her Bio on github!"

	def follow(url,str):
		url_new = url + '?tab=' + str

		try:
			soup = BeautifulSoup(urllib2.urlopen(url_new).read(), 'html.parser')
		except Exception:
			print 'Connection Error!'
			exit()

		user_names = soup.find_all('span', {'class': 'f4 link-gray-dark'})

		for uname in user_names:
			ustring = '-> ' + uname.string
			try:
				print ustring
			except:
				continue
		print ''



	def contributions(soup):
		"""
		Returns the contributions done by user in given Period.
		"""
		# TODO: Generates error. Needs modification
		print "\nContributions of User\n"

		totalContributions = soup.find('div' , {'class' : 'js-contribution-graph'}).find('h2',{'class' : 'f4 text-normal mb-3'}).text
		print "Total contributions last year",totalContributions.split()[0]


		Streaks = soup.find('svg' , {'class' : 'js-calendar-graph-svg'}).find_all('rect')
		longestStreak = 0
		streakList = []
		for streak in Streaks:
			streakList.append(int(streak['data-count']))
			longestStreak = max(int(streak['data-count']),longestStreak)
		print "Longest Streak: ",longestStreak

		print "Total contributions last weeks: ",sum(streakList[-7:])


	def popularRepos(soup):
		"""
		Returns Public repositories of the user.
		"""
		popularRepo = soup.find_all('span' , {'class': 'repo js-repo'})

		if not popularRepo:
			print 'No public repositories for the given user.'
			return
		desc= soup.findAll('p',{'class':'pinned-repo-desc text-gray text-small d-block mt-2 mb-3'})
		stars= soup.findAll('p',{'class':'mb-0 f6 text-gray'})
		length= len(popularRepo)
		countPopularRepo =1
		for i in range(0,length):
			print str(countPopularRepo) + ': '
			countPopularRepo = countPopularRepo+1
			print 'Name :' + popularRepo[i].text
			print 'Description :' + desc[i].text
			descriptions = list(stars[i].stripped_strings)
			description = "\nLanguage : ".join(descriptions) if descriptions else ""
			print "Stars :" +description


	def userdesc(soup):
		try:
			desc= soup.find('div',{'class':'user-profile-bio'}).text
			print "\nUsers Bio:",desc
		except Exception:
			print "\nUsers Bio: This User doesn\'t have a bio"

	print "\nUsers Info\n"
	profileInfo(soup)
	# followers(url)
	contributions(soup)
	print "\nUsers Popular Repositories\n"
	popularRepos(soup)
	userdesc(soup)

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
