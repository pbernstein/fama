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
import send_generic_email_attachment as send_email


def dprint(self,debug):
	if debug == 1:
		print self


def fulfill(date,test,email,form_type,company_sk,eh_sk):
	
	conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape") 
	cursor = conn.cursor ()

	debug = test
	form = form_type

	print " in html fulfill with "+date, email, form_type, str(company_sk)

	cursor.execute("select date_id from dates where date = \""+date+"\"") 
	date_id = str(cursor.fetchone()[0])


	# Find Instrumental Set Attributes

	attributes = []
	num_dates = {}
	gaap_date_value = {}
	column_dict = {}
	attribute_col = []

	# Find Companies that filed today

	companies = []

	# NEW DOES NOT CARE ABOUT GAAP VALUE

	cursor.execute(" select c.cik, c.name, c.company_sk, eh.eh_sk,eh.period from company c,  extract_history eh  where c.company_sk = "+str(company_sk)+" and cast(c.cik as unsigned) = cast(eh.cik as unsigned) and eh.date_id >= "+date_id+" and eh.form = \""+form_type+"\"  and eh.eh_sk = "+str(eh_sk)+" order by name")
	print " select c.cik, c.name, c.company_sk, eh.eh_sk,eh.period from company c,  extract_history eh  where c.company_sk = "+str(company_sk)+" and c.cik = eh.cik and eh.date_id >= "+date_id+" and eh.form = \""+form_type+"\"  and eh.eh_sk = "+str(eh_sk)+" order by name"



	results = cursor.fetchall()
	for result in results:
		companies.append([result[1], result[0],result[2],result[3],result[4]])

	num_companies = str(len(companies))
	if num_companies == "0":
		print "running post check"
		cursor.execute(" select c.cik, c.name, c.company_sk, eh.eh_sk,eh.period from company c,  extract_history eh  where c.company_sk = "+str(company_sk)+" and eh.date_id >= "+date_id+" and eh.form = \""+form_type+"\"  and eh.eh_sk = "+str(eh_sk)+" order by name")
		results = cursor.fetchall()
		for result in results:
			companies.append([result[1], result[0],result[2],result[3],result[4]])
		num_companies = str(len(companies))
		
	print "num companies in html = "+num_companies


	# Fulfill!

	for company in companies:
		cik = company[1]
		name_cik = str(int(cik))
		company_name = company[0]
		company_sk = company[2]
		eh_sk = company[3]
		period = company[4]


	

		company_name = company_name.replace(" ","_").replace("/","-").replace(".","").replace("&","AND").replace(",","").replace("(","").replace(")","")
		print "Fulfilling Company HTML :"+company_name

		output = []

		cursor.execute("select exchange, symbol from symbol where "+str(date_id)+" >= start_date_id and "+str(date_id)+" < end_date_id and cik = \""+str(cik)+"\"") 
		result = cursor.fetchone()
		try:
			exchange = result[0]
			symbol = result[1]
		except:
			exchange = "MISSING"
			symbol = "MISSING"
			print "no symbol found for "+company_name
			continue # TAKE THIS OUT TO FULFILL RECORDS WITH MISSING SYMBOLS


		html_path = "/media/data/investments/data/edgar/forms/rss/loaded/html/"+date.replace("-","")+"/"+cik+"/"
		print "looking here for files "+html_path
		for file in sorted(glob.glob( os.path.join(html_path, '*.html') )):
			print "in html load file "+html_path+"/"+file
			local_fn = file[file.rindex("/")+1:]
			server_fn = symbol+"_"+form+"_"+period+".html"
			print local_fn
			
			try:
				print "scp "+html_path+"/"+local_fn+"   /master/filings/"+date+"/"+server_fn
				os.system("mkdir -p   /media/data/master/filings/"+date)
				os.system("cp "+html_path+"/"+local_fn+"   /media/data/master/filings/"+date+"/"+server_fn)

				if 1 == 1:
					print "attempting to load "+html_path+"/"+local_fn +" to S3 filings/"+server_fn
					try:
						fn_vec = local_fn.split("_")
						local_fn = fn_vec[0]+"_"+fn_vec[1]
						s3.s3_load(html_path+"/"+local_fn,"filings/"+server_fn)
						print "S3 load success to filings/"+server_fn
					except:
						print "S3 load failed "
						print fn, "filings/"+server_fn

			except:
				print "HTML FTP Failed!"
				pass


	cursor.close()
	conn.commit()	
	conn.close()
		





if __name__ == '__main__':
        date = sys.argv[1]
	try:
		test = sys.argv[2]
	except:
		test = 0
	try:
		email = sys.argv[3]
	except:
		email = 0
	try:
		company_sk = sys.argv[4]
	except:
		company_sk = ""
	try:
		eh_sk = sys.argv[5]
	except:
		eh_sk = ""
	#print date,test,email,"10-Q",company_sk
	fulfill(date,test,email,"10-Q",company_sk,eh_sk)
	fulfill(date,test,email,"10-K",company_sk,eh_sk)
	fulfill(date,test,email,"8-K",company_sk,eh_sk)
		


	
