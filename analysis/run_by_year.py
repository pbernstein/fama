#!/usr/bin/python

#
# Usage:

import sys
import os
import os.path
from subprocess import call
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db


conn = db.get_conn()
cursor = conn.cursor()


year = sys.argv[1]
cursor.execute("select date from dates where date > '"+year+"-01-01' and date < '"+year+"-12-31' and weekend = 'Weekday'")
results = cursor.fetchall()
for result in results:
        date = str(result[0])
	call(["/home/peter/work/analysis/run_daily.ksh","30000",date])




cursor.close()



