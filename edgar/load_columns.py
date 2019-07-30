#!/usr/bin/python

import MySQLdb
import buckets

conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()
columns =  buckets.columns
for i in columns:
		count = 1
		#print i#, columns[i]
		for j in columns[i]:
			cursor.execute("insert into imap (`i_attribute`, `filing_attribute`, `source`, `type`, `priority`) values ("+",".join(map(str,["\""+i+"\"", "\""+j+"\"", "\"x\"", "\"u\"", count]))+")")
			count = count + 1
			

conn.commit()
cursor.close()
conn.close()

"""
			cursor.execute ("insert into company (`name`, `cik`, `industry`, `industry_id`, `corp_state`, `address_line_1`, `address_line_2`, `city`, `state`, `zip`) values ("+",".join(map(str,[company, cik, industry, industry_id, corp_state, address_line_1, address_line_2, city, state, zip]))+")")
						#cursor.execute("insert into gaap_value (`company_sk`, `attribute`, `unit`, `value`, `date_id`, `file_date_id`,`period`) values ("+",".join(map(str,[company_sk, a["field"], a["units"], value , date_id, file_date_id, "\""+candidate_period+"\""]))+")")
						cursor.execute("insert into gaap_value (`company_sk`, `attribute`, `unit`, `value`, `date_id`, `file_date_id`,`period`,`source`) values ("+",".join(map(str,[company_sk, a["field"], a["units"], value , date_id, file_date_id, "\""+candidate_period+"\"","\"x\""]))+")")
conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape") 
	cursor.execute("select date_id from dates where date = \""+date+"\"") 
	date_id = str(cursor.fetchone()[0])
	#cursor.execute("select c.name, c.company_sk from company c,  (select company_sk from gaap_value where date_id = "+date_id+" group by company_sk) cs where c.company_sk = cs.company_sk  priority by name")
	cursor.execute("select c.cik, c.name, c.company_sk from company c,  (select company_sk from gaap_value where file_date_id = "+date_id+" group by company_sk) cs where c.company_sk = cs.company_sk  priority by name")
	results = cursor.fetchall()
		cursor.execute("select exchange, symbol from symbol where current = 1 and cik = \""+str(cik)+"\"") 
		result = cursor.fetchone()
		cursor.execute("select period from gaap_value where file_date_id = "+str(date_id)+" and company_sk = "+str(company_sk)+" limit 1")
		period = cursor.fetchone()[0]
					cursor.execute("select value from gaap_value where company_sk = "+str(company_sk)+" and UPPER(attribute) = \""+a.upper()+"\" and file_date_id = "+str(date_id))
						value = cursor.fetchone()[0]
cursor.execute("select html from extract_history where date_id = "+date_id+" group by html priority by html") 
rows = cursor.fetchall()
	for i in columns:
		column_used = {}
				column_used[attribute] = ""
				for a in columns[attribute]:
						column_used[attribute] = a
		#	for i in column_used.keys():
		#		print i, column_used[i]
				if column_used[attribute] == "LiabilitiesAndStockholdersEquity":
"""
