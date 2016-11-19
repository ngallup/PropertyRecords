#!/usr/bin/python

import mechanize
import re
import string

class TulsaAssessor(object):
	url = 'http://www.assessor.tulsacounty.org/assessor-property-search.php'

	# Initialize browser via mechanize
	def __init__(self):
		self.br = mechanize.Browser()
		self.pageHistory = []
	
	# For navigating past the first page on the Tulsa Assessor and getting to
	# the searches page
	def acceptTerms(self):
		front = self.br.open(self.url)
		self.br.select_form(nr=0)
		searchPage = self.br.submit()

		self.pageHistory.append(front)
		self.pageHistory.append(searchPage)

		return front, searchPage

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
		

if __name__ == '__main__':
	assessor = TulsaAssessor()
	front, search = assessor.acceptTerms()

#	print	assessor.parseAddress('8234 South Toledo Ave.') #DELETE

	afterSearch =  assessor.searchByAddress('8234 S Toledo Ave')
	with open('aftersearch.html', 'w') as searchFile:
		searchFile.write(afterSearch.read())

