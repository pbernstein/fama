#!/usr/bin/python
	

import sys
import re
import glob
import os

import MySQLdb
import buckets
import time
from time import strptime
import shutil
import send_generic_email_attachment as send_email


conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape") 
cursor = conn.cursor ()

cursor.execute("select gaap_sk, value,attribute from gaap_value where source = 'h' and file_date_id = 8445")
results = cursor.fetchall()
for result in results:
	gaap_sk = result[0]
	value = result[1]
	attribute = result[2]
	if gaap_sk and value.find(",") != -1 or value.find("$") != -1 or value.find(")") != -1 or attribute[0] == " " or attribute[len(attribute)-1] == " ":
		#print value
		value = value.replace(",","")
		value = value.replace("$","")
		value = value.replace(")","")
		attribute = attribute.lstrip().rstrip()
		#print "update gaap_value set value = "+value+" where gaap_sk = "+str(gaap_sk)
		cursor.execute("update gaap_value set value = '"+value+"' where gaap_sk = "+str(gaap_sk))
		cursor.execute("update gaap_value set attribute = '"+attribute+"' where gaap_sk = "+str(gaap_sk))
		conn.commit()	
				
		
cursor.close()
conn.commit()	
conn.close()




