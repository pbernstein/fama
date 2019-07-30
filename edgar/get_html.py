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
import cleanse
import send_generic_email_attachment as send_email


#id = hashlib.md5(url + title).hexdigest()
conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()




# Every 10 minutes, check
url = 'http://www.sec.gov/Archives/edgar/xbrlrss.all.xml'


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
	if feed['edgar_formtype'] == '10-Q': # or feed['edgar_formtype'] == '10-K': 
		url = feed['id']
		file =  str(url[url.rindex("/")+1:])
		#name = feed['description']
		name = feed['edgar_companyname']
		new_file = 0
		cik = ""
		company_sk = ""
		cik = feed['edgar_ciknumber']
		if cik == "":
			print "No CIK!?!!?"
			print "Name = "+str(name)
			exit(1)	
		#print "name = "+name
		#for i in feed:
		#	print i, feed[i]
		try:
			file_time = feed['published_parsed']
		except:
			file_time = datetime.now()	
		period = feed['edgar_period']
		try:
			file_date = str(datetime.fromtimestamp(time.mktime(file_time)).date())
		except:
			file_date = str(datetime.today().date()) 
       		#print " select company_sk from company where cik = \""+str(cik)+"\""
       		cursor.execute(" select company_sk from company where cik = \""+str(cik)+"\"")
		try:
		        company_sk = cursor.fetchone()[0]
			#print "csk = "+str(company_sk)
       			#print " select eh_sk from extract_history where company_sk = "+str(company_sk)+" and period = \""+str(period)+"\";"
       			cursor.execute(" select eh_sk from extract_history where company_sk = "+str(company_sk)+" and period = \""+str(period)+"\"")
		        result = cursor.fetchone()[0]
			try:
				#print "result = "+str(result)
				test = result
			except:
				result = None
			if result == None:
				new_file = 1
				#  This means that I didn't find this period for this company
				#  Therefore, i load the file
		except:
	       		#print " select company_sk from company where cik = \""+str(cik)+"\""
			new_file = 1
			#  This means that I didn't find this CIK in the table, which means i'm not aware of this company and I should load the file


		if 1 == 1:
			print "name = "+name
			#zip_name = temp_path + name.replace(" ","").replace('/',"").replace('\',"")+".zip"
			zip_name = temp_path + name.replace(" ","").replace('/',"").replace('\\',"")+".zip"
			print "url = "+url

			call(["rm","-r", temp_path[:-1]])
			call(["mkdir","-p",temp_path[:-1]])
			call(["wget", "-q", "-O", zip_name, url])
			call(["unzip","-q", "-d",temp_path, zip_name])
			for file in sorted(glob.glob( os.path.join(temp_path, '*[0-9].xml') )):
				# load the xbrl file
				print "Loading :"+file, file_date	
				cleansed_file = cleanse.cleanse(file)	

				fn = cleansed_file[cleansed_file.rindex("/")+1:]
				loaded_fn = loaded_path + fn
				html_fn = loaded_path + "html/"+fn+".html"
				error_fn = error_path + fn
					# Pull down and save off their html filing for QA purposes	
				if 1 == 1:
					try:
						link = feed['link']
						print "pulling link: "+link
						call(["wget", "-q", "-O", temp_path+"index.htm", link])
						f = open(temp_path+"index.htm")
						found = 0
				                for line in f:
							if line.find("10q") != -1 and line.find("htm"):
								print "found 10q htm"
								htm_link = line[line.index('a href="')+8:line.rindex('"')]
								htm_link = "http://www.sec.gov"+htm_link
								print "Pulling html link: "+htm_link
								call(["wget", "-q", "-O",html_fn, htm_link])
								print "10q html Pulled!"
				                f.close()
	
					except:
						print "failed to send 10q htm"
						exit(0)
						pass



cursor.close()
conn.commit()
conn.close()


