#!/usr/bin/python

#
# Usage:


import sys
import feedparser


def get_cik():
	url = 'http://www.sec.gov/Archives/edgar/xbrlrss.all.xml'
	d = feedparser.parse(url)
	list = []
	for feed in d['entries']:
			try:
				cik = feed['edgar_ciknumber']
				if cik == "":
					print "No CIK!?!!?"
					print "Name = "+str(name)
					exit(1)	
				list.append(cik)
			except:
				#print "no cik?!"
				#for row in feed:
				#	print feed[row]
				pass

	return list

if __name__ == '__main__':
	list = get_cik()
	print list
	
