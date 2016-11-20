#!/usr/bin/python

import mechanize
import re
import string
from bs4 import BeautifulSoup
from unittest.signals import _results

class TulsaAssessor(object):
	url = 'http://www.assessor.tulsacounty.org/assessor-property-search.php'

	# Initialize browser via mechanize
	def __init__(self):
		self.br = mechanize.Browser()
		self.pageHistory = []
		self.name = ''
	
	# For navigating past the first page on the Tulsa Assessor and getting to
	# the searches page
	def acceptTerms(self):
		front = self.br.open(self.url)
		self.br.select_form(nr=0)
		searchPage = self.br.submit()

		self.pageHistory.append(front)
		self.pageHistory.append(searchPage)

		return front, searchPage

	def parseNames(self, names):
		# parseNames parses out the owner names taken from the assessor page
		# and returns a list of the names in a format for easy re-use
		# Will probably need to be rewritten to handle fringe cases
		
		lastname, firstname = names.split(',')
		firstname = firstname.split('AND')
		firstname = [each.split() for each in firstname]
		
		nameList = [firstmid for firstmid in firstname]
		for firstmid in nameList:
			firstmid.append(lastname)
		
		return nameList
	def parseAddress(self, address):
		# 8234 S. Toledo Ave
		# Needs to handle cardinal abbreviation/expansion and optional
		# punctuation.  Needs to handle street type abbreviation/expansion
		# and optional punctuation.  Currently hardcoded

		# Dictionary lookup table of abbreviations and expansions
		dirDic = {
			'north' : 'N',
			'south' : 'S',
			'east'  : 'E',
			'west'  : 'W',
			}
		suffDic = {} # This will need to be populated at some point
		
		noPunc = address.translate(None, string.punctuation)
		streetno, direction, streetname, suffix = noPunc.split()

		# Begin parsing and normalizaing address
		if len(direction) > 1:
			try:
				direction = dirDic[direction.lower()]
			except:
				print "Address error.  Street direction unrecognized."
		else:
			direction = direction.upper()

		# Forcibly return the correct suffix (fix later)
		suffix = 'AV'
		return streetno, direction, streetname, suffix

	# Populate relevant fields to search by property address
	def searchByAddress(self, address):
		streetno, direction, streetname, suffix = self.parseAddress(address)

		self.br.select_form(nr=0)
		self.br['streetno'] = streetno
		self.br['predirection'] = [direction]
		self.br['streetname'] = streetname
		self.br['streettype'] = [suffix]

		page = self.br.submit(name='subaddr')
		self.pageHistory.append(page)

		return page 
	
	# For parsing the search results page as a filelike object and retrieving
	# the name of the owner for future use
	def getName(self, searchResults):
		results = searchResults.read()
		
		
		soup = BeautifulSoup(results, "html.parser")
		
		# Begin parsing the "quick facts" table data
		table = soup.find('table')
		newTable = table.find_all('tr')
			
		# Convert table into useable list
		tableContents = [each.find_all('td') for each in newTable]
		tableContents = [[elem.get_text().encode('ascii', 'replace') for elem in each] for each in tableContents]
		
		# Grab owner property name(s)
		name = tableContents[3][1]
		nameList = self.parseNames(name)
				
		return nameList
		

if __name__ == '__main__':
	assessor = TulsaAssessor()
	front, search = assessor.acceptTerms()

#	print	assessor.parseAddress('8234 South Toledo Ave.') #DELETE

	afterSearch =  assessor.searchByAddress('8234 S Toledo Ave')
#	with open('aftersearch.html', 'w') as searchFile:
#		searchFile.write(afterSearch.read())

	assessor.getName(assessor.br.response()) #Change
