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


#xbrl_file = sys.argv[1]
symbol_list = []
conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()


file=sys.argv[1]
date=sys.argv[2]
form=sys.argv[3]

fail_fn = file.replace("reload/","reload/fail/")
complete_fn = file.replace("reload/","reload/complete/")



if 1 == 1:
	print "Reloading "+file				
	f = open(file)
	cik = ""
	for record in f:

                # Populate Company Info

                if record.find("CENTRAL INDEX KEY:") != -1:
                        cik = "\""+record.split("\t").pop().replace("\n","")+"\""

		if record.find("CIK") != -1:
			cik = record[record.index(">")+1:record.rindex("</")]

		if cik != "":
			break

	print "cik = "+cik

		
	cursor.execute(" select company_sk, name from company where cik = \""+str(cik)+"\"")
	try:
		result = cursor.fetchone()
		company_sk = result[0]
		name = result[1]
		print "name = "+name
	except:
		print "Can't find company"
		shutil.move(file,fail_fn)
		sys.exit(0)

	cursor.execute(" select symbol from symbol where current = 1 and cik = \""+str(cik)+"\"")
	try:
		symbol = cursor.fetchone()[0]
	except:
		print " select symbol from symbol where current = 1 and cik = \""+str(cik)+"\""
		print "Can't find symbol"
		shutil.move(file,fail_fn)
		sys.exit(0)

	symbol_list.append(symbol)
	print "csk = "+str(company_sk)
	print "name = "+name

	cursor.execute("select date_id from dates where date = \""+str(date)+"\"")
	date_id = cursor.fetchone()[0]
	print "date = "+str(date)

	print "form = "+form
	if form == "8-K":
		print "fulfilling html in prod_reload "+name 
		#os.system("/home/peter/work/edgar/fulfill_html.py "+str(date)+" 0 0 "+str(company_sk))
		fulfill_html.fulfill(file_date,0,0,form,company_sk,eh_sk)


	else:
		#print "fulfilling everything because I'm not an 8-K"
		#cursor.execute("delete from gaap_value where file_date_id = "+str(date_id)+" and company_sk = "+str(company_sk))
		#conn.commit()
		#cursor.execute("delete from ins_value where date_id = "+str(date_id)+" and company_sk = "+str(company_sk))
		#conn.commit()


		#os.system("/home/peter/work/edgar/cleanse.py "+file+" "+symbol)

		#os.system("/home/peter/work/edgar/xbrl_load_quarter.py "+file+".cleansed \""+name+"\" "+cik+" "+date+" "+form+" "+symbol)



		#os.system("/home/peter/work/edgar/fulfill_html.py "+str(date)+" 0 0 "+str(company_sk))
		#os.system("/home/peter/work/edgar/fulfill_raw.py "+str(date)+" 0 0 "+str(company_sk))
		fulfill_html.fulfill(file_date,0,0,form,company_sk,eh_sk)
		fulfill_raw.fulfill_raw(file_date,0,0,form,company_sk,eh_sk,"","")
		num_companies = fulfill_id.fulfill(file_date,0,0,form,company_sk,eh_sk,"","")

		#os.system("/home/peter/work/edgar/fulfill_id.py "+str(date)+" 1 0 "+str(company_sk))
		#print "fulfilled id stuff, now I'm running publish with "+date, form, str(company_sk)
		publish_id.fulfill(date,form,company_sk)


		#os.system("/home/peter/qa/regression/display_instrumental.ksh  "+str(date)+" "+symbol)
	shutil.move(file,complete_fn)

cursor.close()
conn.close()
