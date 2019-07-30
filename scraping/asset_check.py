#!/usr/bin/python
import os
import sys
import glob
from time import strptime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db



table="asset_value"
conn = db.get_conn()
cursor = conn.cursor()
for did in range(364, 3986):
	cursor.execute ("select date, day_of_week from dates where date_id = "+str(did))
	result = cursor.fetchone()
	date = result[0]
	day_of_week = result[1]
	sys.stdout.write(str(date))
 	sys.stdout.write("\t")	
	sys.stdout.write(str(day_of_week[:3]))
 	sys.stdout.write("\t")	
	cursor.execute ("select date_id, exchange, count(*) as cnt from asset_value where date_id = "+str(did)+" group by date_id, exchange")
	results = cursor.fetchall()
	for counts in results:
		sys.stdout.write(str(counts[2]))
	 	sys.stdout.write(" ")	
	print


cursor.close()
conn.commit()
conn.close()



