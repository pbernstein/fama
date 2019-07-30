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
from subprocess import check_output
import feedparser
import hashlib
import MySQLdb
import shutil
import utility
import xbrl_load_quarter
import html_load_gaap
import cleanse
import send_generic_email_attachment as send_email
from refulfill import fulfill_raw as fulfill_raw
from refulfill import fulfill_html as fulfill_html
import table_reader as table_reader
import tweet
import clean_txt_html
import clean_txt_xbrl


conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()



cursor.execute("select eh.eh_sk, eh.form, d.date, c.company_sk, eh.date_id from extract_history eh, company c, dates d where eh.date_id = d.date_id and eh.cik = c.cik and eh.date_id >= 8402 order by eh.date_id")
results = cursor.fetchall()
for result in results:
	if not os.path.exists("/tmp/refulfill_run"):
		print "exit"
		sys.exit(0)
	org_eh_sk = str(result[0])
	form = str(result[1])
	file_date = str(result[2])
	company_sk = str(result[3])
	file_date_id = str(result[4])
	#cursor.execute("select distinct(eh_sk) from gaap_map where  file_date_id = "+file_date_id+" and company_sk = "+str(company_sk))
	#eh_results = cursor.fetchall()
	#print eh_results
	#print str(len(eh_results))
	#if len(eh_results) > 1:
	#	print "two eh_sk's for "+str(org_eh_sk)+" in gaap_map!"
	#	sys.exit(1)

	#try:			
	#	eh_sk = str(eh_results[0][0])
	#except:
	#	print "select distinct(eh_sk) from gaap_map where  file_date_id = "+file_date_id+" and company_sk = "+str(company_sk)
	#	print "eh results = "+str(eh_results)
	#	sys.exit(1)
	#print "eh_sk = "+str(eh_sk)
	try:
		fulfill_html.fulfill(file_date,0,0,form,company_sk,org_eh_sk)
	except:
		print "failed html" 	
		sys.exit(1)

	#sys.exit(0)


cursor.close()
conn.commit()
conn.close()



