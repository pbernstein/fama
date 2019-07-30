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


conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()

#date = sys.argv[1]
#cursor.execute("select date_id from dates where date = \""+str(date)+"\"")
#date_id = cursor.fetchone()[0]
#
#cursor.execute(" select  html,form  from extract_history where date_id= "+str(date_id))
#results = cursor.fetchall()
#count = 0 
#for result in results:
#	html = result[0]
#	form = result[1]


path = "/media/data/investments/data/edgar/forms/rss/loaded/reload"
for file in sorted(glob.glob( os.path.join(path, '*10-Q*') )):

# Try looking for the files instead? 
#	need to get name,date	, and form
	#name = "brcm-20121231.xml"
	name = file
	print name
	time_tuple =  time.ctime(os.path.getmtime(name))
	dt_obj = datetime.strptime(time_tuple, "%a %b %d %H:%M:%S %Y")
	date = dt_obj.strftime("%Y-%m-%d")

	
	#result = check_output(["grep","CIK", name])
	#cik = result.split(">")[1].split("<")[0]
	#cursor.execute("select form from extract_history where cik = "+cik)

	result = call(["grep",">10-Q<",name])	
	if result == 1:
		result = call(["grep",">10-K<",name])	
		if result == 1:
			print "couldn't figure out the symbol for "+name
			sys.exit(1)
		else:
			form = "10-K"
	else:
		form = "10-Q"

	

	os.system("/home/peter/work/edgar/prod_reload.py "+name+" "+date+" "+form)
	#count = count + 1
	#if count > 5:
	#	break

cursor.close()
conn.close()
