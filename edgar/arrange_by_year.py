#!/usr/bin/python

#
# Usage:

import sys
import os
import os.path
from subprocess import call
import MySQLdb



conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()

year = sys.argv[1]
cursor.execute("select date from dates where date > '"+year+"-01-01' and date < '"+year+"-12-31' and weekend = 'Weekday'")
results = cursor.fetchall()
for result in results:
        date = str(result[0])
        #print "/home/peter/work/edgar/log_eod.ksh",date
        #call(["/home/peter/work/edgar/log_eod.ksh",date])
        #print "finished:", date
	call(["/home/peter/work/edgar/arrange_history.py",date])




cursor.close()
conn.close()



