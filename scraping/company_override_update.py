#!/usr/bin/python

import os
import glob
import sys
import time
import random
from time import strptime
from subprocess import call
from subprocess import check_output
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db


def fix_me():
		cursor.execute ("SELECT company_sk, name, cik, name_override from company")
		rows = cursor.fetchall()
		for row in rows:
			random.seed()
			company_sk = row[0]
			name = row[1]
			cik = row[2]
			name_override = row[3]
			if name_override == None:
				try:
					result = check_output(["/home/peter/work/scraping/symbol.ksh", "\""+name+"\""])
					symbol = result.split("\n")[1].strip()
					exchange = result.split("\n")[2].strip()

					n = random.random() * 7
					time.sleep(n)


					print "SELECT symbol, exchange, name_override from symbol where symbol = \""+symbol+"\" and exchange = \""+exchange+"\""
					cursor.execute ("SELECT symbol, exchange, name_override from symbol where symbol = \""+symbol+"\" and exchange = \""+exchange+"\"")
					sr = cursor.fetchone()
					print "sr = "+str(sr)
					if sr == None:
						print name +" not found in symbol!"
						
					print "Updating "+name 
		                        cursor.execute ("update company set name_override = \""+sr[2].upper()+"\" where company_sk = "+str(company_sk))
					#break;
					if exchange == "NASDAQ":
						break

						
				except:
				#except cursor.Error, e:
 				#	print "Error %d: %s" % (e.args[0],e.args[1])
					print "Broke on "+name 
					#sys.exit(0)



				

conn = db.get_conn()
cursor = conn.cursor()


fix_me()


cursor.close()
conn.commit()
conn.close()



