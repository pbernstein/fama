#!/usr/bin/python


import sys
import re
import glob
import os

import MySQLdb
import buckets
import time
from time import strptime


	cursor = conn.cursor ()
	output = []

	header = []
	header.append("Company Name")
	header.append("Exchange")
	header.append("Symbol")
	header.append("Quarter")

	cursor.execute("select date_id from dates where date = \""+date+"\"") 
	date_id = str(cursor.fetchone()[0])

	attributes = []
	columns =  buckets.columns

	#for i in columns:
	#	print i, columns[i]
	#exit(0)

	for i in columns:
		attributes.append(i)

	attributes.sort()

	for a in attributes:
		header.append(a)

	output.append(header)

	#print output

	companies = []
#	cursor.execute("select name, company_sk from company where company_sk in (select company_sk from gaap_value where date_id = "+date_id+" group by company_sk) order by name limit 10")
	t0=time.time()
	cursor.execute("select name, company_sk from company where company_sk in (select company_sk from gaap_value where file_date_id = "+date_id+" group by company_sk) order by name")
	print "select name, company_sk from company where company_sk in (select company_sk from gaap_value where file_date_id = "+date_id+" group by company_sk) order by name"
	results = cursor.fetchall()
	#t0=time.time()
	print "company build Elapsed time: "+str(time.time() - t0)
	print results 
	for result in results:
		companies.append([result[0].replace(",",""), result[1]])

	print "num companies = "+str(len(companies))

	count = 0 
	for company in companies:
		row = []
		#cursor.execute("select exchange, symbol from symbol where date_id = "+str(date_id)+" and company_sk = "+str(company[1])) # add a group by symbol here, i could be cartesianing, badly, yell if this is it
		t0=time.time()
		#print "select exchange, symbol from symbol where date_id = "+str(date_id)+" and company_sk = "+str(company[1])+" group by symbol"
		cursor.execute("select exchange, symbol from symbol where date_id = "+str(date_id)+" and company_sk = "+str(company[1])+" group by symbol") 
		results = cursor.fetchall()
		print "results of symbol extract: "+str(results)
		if count > -1:
			print "symbol find Elapsed time: "+str(time.time() - t0)
			print "num attributes = "+str(len(attributes))
		if len(results) > 1:
			print "for date_id = "+str(date_id)+" and company "+company
			print "results of symbol extract: "+str(results)
			print "exiting"
			exit(0)

		try:
			exchange = results[0][0]
			symbol = results[0][1]
		except:
			exchange = "MISSING"
			symbol = "MISSING"
			#continue

		row.append(company[0])
		row.append(exchange)
		row.append(symbol)


		cursor.execute("select period from gaap_value where file_date_id = "+str(date_id)+" and company_sk = "+str(company[1])+" limit 1")
		#print "select period from gaap_value where file_date_id = "+str(date_id)+" and company_sk = "+str(company[1])+" limit 1"
		period = cursor.fetchone()[0]
		row.append(period)
		

		for attribute in attributes:
			try:
				summed_value = 0
				for a in columns[attribute]:
					#t0=time.time()
					cursor.execute("select value from gaap_value where company_sk = "+str(company[1])+" and attribute = \""+a+"\" and file_date_id = "+str(date_id))
					try:
						value = cursor.fetchone()[0]
					except:	
						# print "Can't parse value"
						pass
					try:
						summed_value = summed_value + float(value)
					except:	
						pass
					#if count < 5:
					if count > -1:
						print "value find Elapsed time: "+str(time.time() - t0)
					count = count + 1
				row.append(summed_value)
			except:
				row.append("")
		output.append(row)

	print "output size = "+str(len(output))
	#print output
	fn = "/media/data/investments/data/edgar/fulfillment/ins_"+date+".csv"
	file = open(fn,'w')
	for row in output:
		buffer = ""
		for field in row:
			buffer = buffer + str(field) +","
		#print buffer[:-1]
		file.write(buffer[:-1]+"\n")
	file.close()
		


	cursor.close()
	conn.commit()	
	conn.close()




if __name__ == '__main__':
        date = sys.argv[1]
        fulfill(date)


	
