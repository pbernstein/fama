#!/usr/bin/python
	
import publish_s3 as s3
import sys
import re
import glob
import os

import MySQLdb
import buckets
import time
from time import strptime
import shutil
import send_generic_email_attachment as send_mail



"""
dividend_field = []
cursor.execute("select filing_attribute from imap where i_attribute = \"Dividends\"")
results = cursor.fetchall()
for result in results:
	dividend_field.append(result[0])

inv_field = []
cursor.execute("select filing_attribute from imap where i_attribute = \"Inventory\"")
results = cursor.fetchall()
for result in results:
	inv_field.append(result[0])

"""


def fulfill(date):
	count = 0 
	output = []

	header = []
	header.append("Company Key")
	header.append("Company Name")
	header.append("Exchange")
	header.append("Symbol")
	header.append("Industry Key")
	header.append("Industry Name")
	output.append(header)


        cursor.execute("select date_id from dates where date = \""+date+"\"")
        date_id = str(cursor.fetchone()[0])

	#cursor.execute("select company_sk, symbol, exchange, sic from ins_map group by symbol, exchange")
	cursor.execute("select company_sk, symbol, exchange, sic,cik from symbol_map group by symbol, exchange")

	results = cursor.fetchall()
	companies = []
	for result in results:
		companies.append([result[0],result[1],result[2],result[3],result[4]])


	for company in companies:
		company_sk = company[0]
		symbol = company[1]
		exchange = company[2]
		sic = company[3]
		cik = company[4]

		#print "select c.cik, c.name, sr.sic_name from company c, sic_ref sr, symbol s where c.cik = s.cik and s.sic = sr.sic and c.company_sk = "+str(company_sk)
		#print "select c.cik, c.name, sr.sic_name from company c, sic_ref sr, symbol s where c.cik = s.cik and s.sic = sr.sic and c.cik = "+str(cik)
		try:		
			cursor.execute("select c.cik, c.name, sr.sic_name from company c, sic_ref sr, symbol s where c.cik = s.cik and s.sic = sr.sic and c.company_sk = "+str(company_sk))
			result = cursor.fetchone()
			company_name = str(result[1].replace(",",""))
			sic_name = str(result[2].replace(",",""))
		except:
			continue



		row = []
		row.append(str(int(cik)))
		row.append(company_name)
		row.append(exchange)
		row.append(symbol)
		row.append(sic)
		row.append(sic_name)
		
		output.append(row)

	fn = "/media/data/investments/data/edgar/fulfillment/symbols_"+date+".csv"
	file = open(fn,'w')
	for row in output:
		buffer = ""
		for field in row:
			buffer = buffer + str(field) +","
		#print buffer[:-1]
		file.write(buffer[:-1]+"\n")
	file.close()


	print "Publishing "+fn	
	#os.system("scp -i /home/peter/bin/testserver.pem "+fn+"   ubuntu@50.19.103.62:/master/symbols")
        try:
		print "publishing to s3"
		s3.s3_load(fn,"symbols/"+fn[fn.rindex("/")+1:])
	except:
		print "S3 load failed "
		print fn, "instrumental/"+fn[fn.rindex("/")+1:]






conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape") 
cursor = conn.cursor ()

if __name__ == '__main__':
        date = sys.argv[1]
        fulfill(date)

	
cursor.close()
conn.commit()	

