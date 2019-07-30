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

year = sys.argv[1]

conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()


cursor.execute("select date from dates where date > '"+year+"-01-03' and date < '"+year+"-12-31' and weekend = 'Weekday'")
results = cursor.fetchall()
for result in results:
	date = str(result[0])
	number_date = date.replace("-","")
	year = date.split("-")[0]
	bkp_path = "/master/history/staging/"+year+"/"
	print bkp_path+"eod_"+number_date+".tar.gz"
	if not os.path.exists(bkp_path+"eod_"+number_date+".tar.gz"):
		call(["/home/peter/work/edgar/pull_eod_csi.py",date])
		#print 'call(["/home/ubuntu/work/edgar/pull_eod_csi.py",date])'
	print "finished:", date
	#sys.exit(0)


	

cursor.close()
conn.close()

