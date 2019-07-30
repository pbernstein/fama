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
import filecmp
import fulfill_id as fulfill_id
import fulfill_raw as fulfill_raw
import fulfill_html as fulfill_html
import publish_id as publish_id
import table_reader as table_reader
import time


#xbrl_file = sys.argv[1]
symbol_list = []
conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()




#cursor.execute('select eh.cik, c.company_sk, s.symbol, s.exchange, eh.date_id, eh.eh_sk, eh.form from extract_history eh, symbol s, company c where eh.cik = c.cik and eh.cik = s.cik and s.current = 1  group by eh.eh_sk')
#cursor.execute('select c.company_sk, eh.date_id, eh.eh_sk, eh.form from extract_history eh, company c where eh.cik = c.cik group by e.eh_sk')
cursor.execute('select c.company_sk, eh.eh_sk, eh.form, eh.name from extract_history eh, company c where eh.cik = c.cik group by eh.eh_sk order by eh.eh_sk, eh.date_id')
results = cursor.fetchall()
count = 0 
for result in results:
	count = count + 1
	company_sk = str(result[0])
	eh_sk = str(result[1])
	form = result[2]
	name = result[3]
	cursor.execute('select d.date from gaap_value g, dates d where g.eh_sk = '+eh_sk+'  and g.file_date_id = d.date_id limit 1')
	try:
		file_date = str(cursor.fetchone()[0])
	except:
		print "Found nothin' for : \""+name+"\"  "+ str(company_sk), file_date, str(eh_sk), form

	print "Running "+name+" for date: "+file_date
		
	try:
		#start = time.time()
		#fulfill_html.fulfill(file_date,0,0,form,company_sk,eh_sk)
		#print time.time() - start
		#start = time.time()
		fulfill_raw.fulfill_raw(file_date,1,0,form,company_sk,eh_sk,"","")
		num_companies = fulfill_id.fulfill(file_date,1,0,form,company_sk,eh_sk,"","")
		#print time.time() - start
	except:
		print "Failed fulfilling for : \""+name+"\"  "+ str(company_sk), file_date, str(eh_sk), form


	#publish_id.fulfill(date,form,company_sk)
	#if count > 10:
	if  os.path.isfile("/home/peter/work/edgar/run") == False: 
		break

cursor.close()
conn.close()
