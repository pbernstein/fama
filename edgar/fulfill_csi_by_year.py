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
#cursor.execute("select date from dates where date > '"+year+"-01-01' and date < '"+year+"-12-31' and weekend = 'Weekday'")
cursor.execute("select date from dates where date > '"+year+"-02-20' and date < '"+year+"-12-31' and weekend = 'Weekday'")
results = cursor.fetchall()
for result in results:
        date = str(result[0])
        month = int(date.split("-")[1])
        call(["/home/peter/work/edgar/log_csi.ksh",date])
        print "finished:", date




cursor.close()
conn.close()



