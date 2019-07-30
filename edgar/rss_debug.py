#!/usr/bin/python

#
# Usage:


import sys
import time
from datetime import datetime
import os
import os.path
import glob
from subprocess import call
import feedparser
import hashlib
import MySQLdb
import shutil
import xbrl_load_quarter

#id = hashlib.md5(url + title).hexdigest()
conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()




# Every 10 minutes, check
url = 'http://www.sec.gov/Archives/edgar/xbrlrss.all.xml'
#url = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-2013-07.xml'



d = feedparser.parse(url)


# It will have 200 entries

path = "/media/data/investments/data/edgar/forms/rss/"
temp_path = "/media/data/investments/data/edgar/forms/temp/"
loaded_path = "/media/data/investments/data/edgar/forms/rss/loaded/"
error_path = "/media/data/investments/data/edgar/forms/rss/error/"
date = str(unicode(datetime.today())[:10]).replace("-","")
cursor.execute(" select date_id from dates where date = \""+str(date)+"\"")
row = cursor.fetchone()
date_id = row[0]
count = 0

for feed in d['entries']:

		if feed['edgar_formtype'] == '10-Q' or feed['edgar_formtype'] == '10-K' or feed['edgar_formtype'] == "8-K": 
			for object in feed:
				print object, feed[object]
		sys.exit(0)
		"""
		#if feed['edgar_formtype'] == '10-Q' or feed['edgar_formtype'] == '10-K': 
		url = feed['id']
		file =  str(url[url.rindex("/")+1:])
		#name = feed['description']
		name = feed['edgar_companyname']
		fd = feed['edgar_filingdate']
		new_file = 0
		cik = ""
		company_sk = ""
		cik = feed['edgar_ciknumber']
		if cik == "":
			print "No CIK!?!!?"
			print "Name = "+str(name)
			exit(1)	
		#print "name = "+name
		#print cik
		#file_time = feed['published_parsed']
		if feed['edgar_formtype'] == "8-K":
			for object in feed:
				print object, feed[object]
			sys.exit(1)
		try:
			period = feed['edgar_period']
		except:
			#for object in feed:
				#print object, feed[object]
			#sys.exit(1)
			continue
		print feed['edgar_formtype']+": "+name, period, fd
		#print "period = "+period
		link = feed['link']
		#call(["wget", "-q", "-O", temp_path + "feed.zip", url])
		#call(["wget", "-q", "-O", "index.htm", link])
		#f = open("index.htm")
		#for line in f:
		#	if line.find("10q.htm") != -1:
		#		print line
		#		htm_link = line[line.index('a href="')+8:line.rindex('"')]
		#		htm_link = "http://www.sec.gov"+htm_link
		#		print htm_link
		#		call(["wget", "-q", "-O", "10q.htm", htm_link])
		#f.close()	
		count = count + 1
		#if count == 4:
		#	break
		"""
		"""
		if name.find("AMERISOURCEBERGEN") != -1:
			for attribute in feed:
				print attribute, feed[attribute]
		"""

print "count = "+str(count)
