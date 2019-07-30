#!/usr/bin/python

#
# Usage:

import re
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


conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()




file_date = sys.argv[1]
year = file_date.split("-")[0]

date = file_date.replace("-","")

filing_path = "/media/data/master/filings"
parsed_path = "/media/data/master/parsed"
new_filing_path = "/media/data/master/history/filings/"+year
new_parsed_path = "/media/data/master/history/parsed/"+year

cursor.execute("select date_id from dates where date = \""+str(date)+"\"")
row = cursor.fetchone()
date_id = row[0]


for file in sorted(glob.glob( os.path.join(filing_path+"/"+file_date, '*.html') )):
	presymbol = file.split("_")[0]
	symbol = presymbol[presymbol.rindex("/")+1:]
	fn = file[file.rindex("/")+1:]
	try:
		#print " select exchange from symbol where symbol = \""+symbol+"\" and end_date_id > "+str(date_id)+" and start_date_id <= "+str(date_id)
		if year == "2012":
			cursor.execute(" select exchange from symbol where symbol = \""+symbol+"\" and end_date_id > "+str(date_id)+" and start_date_id <= "+str(date_id))
		else:
			#print " select exchange from csi_symbols where symbol = \""+symbol+"\" and date_id = "+str(date_id)
			cursor.execute(" select exchange from csi_symbols where symbol = \""+symbol+"\" and date_id = "+str(date_id))
		try:
			row = cursor.fetchone()
			exchange = row[0]
		except:
			cursor.execute(" select exchange from csi_symbols where symbol = \""+symbol+"\" and date_id = "+str(date_id))
			row = cursor.fetchone()
			exchange = row[0]

		#print file, symbol, exchange
		#print file,new_path+"/"+exchange+"/"+fn

		shutil.move(file,new_filing_path+"/"+exchange+"/"+fn)

		#sys.exit(0)
	except:
		print "symbol couldn't find an exchange!!!!!: "+file, symbol
		sys.exit(0)



for file in sorted(glob.glob( os.path.join(parsed_path+"/"+file_date, '*.csv') )):
	presymbol = file.split("_")[0]
	symbol = presymbol[presymbol.rindex("/")+1:]
	fn = file[file.rindex("/")+1:]
	try:
		if year == "2012":
			cursor.execute(" select exchange from symbol where symbol = \""+symbol+"\" and end_date_id > "+str(date_id)+" and start_date_id <= "+str(date_id))
		else:
			cursor.execute(" select exchange from csi_symbols where symbol = \""+symbol+"\" and date_id = "+str(date_id))
		try:
			row = cursor.fetchone()
			exchange = row[0]
		except:
			cursor.execute(" select exchange from csi_symbols where symbol = \""+symbol+"\" and date_id = "+str(date_id))
			row = cursor.fetchone()
			exchange = row[0]

		shutil.move(file,new_parsed_path+"/"+exchange+"/"+fn)
		#sys.exit(0)
	except:
		print "in parsed symbol couldn't find an exchange!!!!!: "+file, symbol
		sys.exit(0)



cursor.close()
conn.commit()
conn.close()



