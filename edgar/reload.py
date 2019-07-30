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


#xbrl_file = sys.argv[1]
symbol_list = []
conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()


file=sys.argv[1]
date=sys.argv[2]
form=sys.argv[3]




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

	cursor.execute(" select symbol from symbol where current = 1 and cik = \""+str(cik)+"\"")
	try:
		symbol = cursor.fetchone()[0]
	except:
		print "Can't find symbol"
		sys.exit(1)
	symbol_list.append(symbol)
	cursor.execute(" select company_sk, name from company where cik = \""+str(cik)+"\"")
	try:
		result = cursor.fetchone()
		company_sk = result[0]
		name = result[1]
	except:
		print "Can't find company"
		sys.exit(1)

	print "csk = "+str(company_sk)
	print "name = "+name
	cursor.execute("select date_id from dates where date = \""+str(date)+"\"")
	date_id = cursor.fetchone()[0]
	print "date = "+str(date)
	print "date_id = "+str(date_id)
	cursor.execute("delete from gaap_value where file_date_id = "+str(date_id)+" and company_sk = "+str(company_sk))
	conn.commit()
	cursor.execute("delete from ins_value where date_id = "+str(date_id)+" and company_sk = "+str(company_sk))
	conn.commit()



	os.system("/home/peter/work/edgar/cleanse.py "+file+" "+symbol)

	os.system("/home/peter/work/edgar/xbrl_load_quarter.py "+file+".cleansed \""+name+"\" "+cik+" "+date+" "+form+" "+symbol)



	os.system("/home/peter/work/edgar/fulfill_id.py "+str(date)+" 1 0 "+str(company_sk))
	os.system("/home/peter/work/edgar/fulfill_raw.py "+str(date)+" 1 0 "+str(company_sk))

	os.system("/home/peter/qa/regression/display_instrumental.ksh  "+str(date)+" "+symbol)

cursor.close()
conn.close()
