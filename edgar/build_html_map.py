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


def dprint(self,debug):
	if debug == 1:
		print self


def map(date):
	
	conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape") 
	cursor = conn.cursor ()


	#print " in fulfill with "+date, email, form_type, str(company_sk)

	cursor.execute("select date_id from dates where date = \""+date+"\"") 
	date_id = str(cursor.fetchone()[0])

	cursor.execute("select company_sk,form, attribute, value,period  from ins_value where date_id = "+date_id)
	results = cursor.fetchall()
	for result in results:
		csk = str(result[0])
		form = result[1]
		attribute = result[2]
		value = result[3]
		period = result[4]
		if value == "NR":
			continue
	
#		print "select gv.attribute  from gaap_value gv, extract_history eh where gv.eh_sk = eh.eh_sk and gv.source = 'h' and gv.file_date_id = "+date_id+" and gv.company_sk = "+csk+" and gv.value = "+value+" and eh.form = '"+form+"' and gv.period = '"+period+"'"
		cursor.execute("select gv.attribute  from gaap_value gv, extract_history eh where gv.eh_sk = eh.eh_sk and gv.source = 'h' and gv.file_date_id = "+date_id+" and gv.company_sk = "+csk+" and gv.value = "+value+" and eh.form = '"+form+"' and gv.period = '"+period+"'") 
		h_results = cursor.fetchall() 
		if h_results:
			print "found match!"
			for h_result in h_results:
				print "h_result = "+str(h_result[0])
				try: 
					h_attribute = h_result[0]
					cursor.execute("select imap_sk from imap where source = 'h' and i_attribute = '"+attribute+"' and filing_attribute = '"+h_attribute+"'")

					imap_result = cursor.fetchone()
					if not imap_result:
				         	#print "insert into imap (company_sk, i_attribute, filing_attribute, source, type, priority, count) values ("+csk+", '"+attribute+"', '"+h_attribute+"', 'h','u',"+str(len(h_attribute))+",0)"
						cursor.execute("insert into imap (company_sk, i_attribute, filing_attribute, source, type, priority, count) values ("+csk+", '"+attribute+"', '"+h_attribute+"', 'h','u',"+str(len(h_attribute))+",0)")
					else:
						print "imap_result = "+str(imap_result[0])
						cursor.execute("update imap set count = count + 1 where imap_sk = "+str(imap_result[0]))
					conn.commit()	
				except:
					print "Died in the loop"
		else:
			#print "no matches found"
			pass
			
			
					
	
				# care about all matches with the shortest attribute name
				# now look for h_result in imap to see if it'ls already there
				# if it is, increment count,
				# if it isn't, add it, mapping h_result to attribute
				
		
	cursor.close()
	conn.commit()	
	conn.close()





if __name__ == '__main__':
        date = sys.argv[1]
	#print date,test,email,"10-Q",company_sk
	map(date)
		


