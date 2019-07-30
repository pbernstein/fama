#!/usr/bin/python


import publish_s3 as s3
import sys
import re
import glob
import os

import buckets
import time
from time import strptime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

# SET GLOBALS



def fulfill_raw(date,test,email,form_type,company_sk,eh_sk,dir,fn):
        conn = db.get_conn()
        cursor = conn.cursor()

	cursor.execute("select date_id from dates where date = \""+date+"\"") 
	date_id = str(cursor.fetchone()[0])

	attributes = []
	form = form_type.replace("/","-").replace("'","-").replace('"',"-")

	companies = []
	company_sk = str(company_sk)


        print "select c.cik, c.name, c.company_sk from company c,  (select company_sk from gaap_value where file_date_id = "+date_id+" group by company_sk) cs, extract_history eh  where c.company_sk = "+str(company_sk)+" and c.company_sk = cs.company_sk and cast(c.cik as unsigned) = cast(eh.cik as unsigned) and eh.date_id >= "+date_id+" and eh.form = \""+form_type+"\"  and eh.eh_sk = "+str(eh_sk)+" order by name"
        cursor.execute("select c.cik, c.name, c.company_sk from company c,  (select company_sk from gaap_value where file_date_id = "+date_id+" group by company_sk) cs, extract_history eh  where c.company_sk = "+str(company_sk)+" and c.company_sk = cs.company_sk and cast(c.cik as unsigned) = cast(eh.cik as unsigned) and eh.date_id >= "+date_id+" and eh.form = \""+form_type+"\"  and eh.eh_sk = "+str(eh_sk)+" order by name")


        results = cursor.fetchall()
        for result in results:
		#print "JAKE "+str(result)
                companies.append([result[1].replace(",",""), result[0], result[2]])

        #print "num companies = "+str(len(companies))

	
	#if test == 0 and len(companies) > 0:
	#	os.system('ssh -i ~/bin/testserver.pem ubuntu@50.19.103.62 "mkdir -p /master/parsed/'+date+'"')
	#if test == 1:
        #       os.system('mkdir -p /media/data/id/refulfill/parsed/'+date)

	#os.system('ssh -i ~/bin/testserver.pem ubuntu@50.19.103.62 "mkdir -p /master/parsed/'+date+'"')

	

        count = 0
        for company in companies:
                print "Raw Fulfilling Company :"+company[0]

		cik = company[1]
		#company_name = company[0].replace(" ","_").replace("/","-").replace(".","").replace("&","AND")
		#company_name = company[0].replace(" ","_").replace("/","-").replace(".","").replace("&","AND").replace(",","").replace("(","").replace(")","").upper()
		company_name = company[0].replace(" ","_").replace("/","-").replace(".","").replace("&","AND").replace(",","").replace("(","").replace(")","").replace('"','').replace("'","").upper()

		#print "company_name raw = "+company_name

                company_sk = company[2]
		company_sk = str(company_sk)

		#cursor.execute("select exchange, symbol from symbol where current = 1 and cik = \""+str(cik)+"\" order by exchange desc limit 1") # <- code a better rule than this
		#cursor.execute("select exchange, symbol from symbol where current = 1 and cik = \""+str(cik)+"\" order by exchange desc, length(symbol)  limit 1") # <- code a better rule than this
		#PMB 0917	
		#print "select exchange, symbol from symbol where "+str(date_id)+" > start_date_id and "+str(date_id)+" < end_date_id and cik = \""+str(cik)+"\" order by exchange desc, length(symbol)  limit 1"
		cursor.execute("select exchange, symbol from symbol where "+str(date_id)+" > start_date_id and "+str(date_id)+" < end_date_id and cik = \""+str(cik)+"\" order by exchange desc, length(symbol)  limit 1")
						# NYSE wins
						# NASDAQ
						# AMEX	
						# the best way to do this would be to also have volume for each symbol.  
                result = cursor.fetchone()
                try:
                        exchange = result[0]
                        symbol = result[1]
                except:
                        exchange = "MISSING"
                        symbol = "MISSING"
			print "no symbol found for"+company[0]
                        continue # TAKE THIS OUT TO FULFILL RECORDS WITH MISSING SYMBOLS


		#print "select period from gaap_value where eh_sk = "+str(eh_sk)+" and file_date_id = "+str(date_id)+" and company_sk = "+str(company_sk)+" limit 1"
		#cursor.execute("select period from gaap_value where eh_sk = "+str(eh_sk)+" and file_date_id = "+str(date_id)+" and company_sk = "+str(company_sk)+" limit 1")
		#print "select period from extract_history where eh_sk = "+str(eh_sk)
		cursor.execute("select period from extract_history where eh_sk = "+str(eh_sk))
                period = cursor.fetchone()[0]

                #target_fn = "/media/data/master/parsed/"+date+'/'+symbol+"_"+form+"_"+period+".csv"
		#if os.path.exists(target_fn):
		#	return

		
		


		header = []
		header.append("Attribute")
		header.append("Value")
		header.append("Date:Instant")
		header.append("Date:RangeStart")
		header.append("Date:RangeEnd")

		attribute_col = []
		value_col = []
		units_col = []
		date_instant_col = []
		date_start_col = []
		date_end_col = []

		attribute_col.append("Company Name")
		value_col.append(company_name)
		date_instant_col.append(date)
		date_start_col.append("")
		date_end_col.append("")

		attribute_col.append("Company Key")
                value_col.append(str(int(cik)))
                date_instant_col.append("")
                date_start_col.append("")
                date_end_col.append("")

		attribute_col.append("Exchange")
		value_col.append(exchange)
		date_instant_col.append(date)
		date_start_col.append("")
		date_end_col.append("")

		attribute_col.append("Symbol")
		value_col.append(symbol)
		date_instant_col.append(date)
		date_start_col.append("")
		date_end_col.append("")

		attribute_col.append("Form")
		value_col.append(form)
		date_instant_col.append(date)
		date_start_col.append("")
		date_end_col.append("")

		attribute_col.append("Quarter Filed")
                value_col.append(period)
                date_instant_col.append(date)
                date_start_col.append("")
                date_end_col.append("")

		#print "here"
                if dir == "": 
			os.system("mkdir -p /media/data/investments/data/edgar/fulfillment/raw/"+date)
                else:
                        os.system('mkdir -p '+dir)
                if fn == "":
	                fn = "/media/data/investments/data/edgar/fulfillment/raw/"+date+"/"+company_name+"_parsed_"+form+"_"+period+".csv"

                else:
                        fn = dir+"/"+fn

	
		file = open(fn,'w')

                new_line = "\r\n" # Windows
                #new_line = "\n" # Linux
                buffer = ""
                for column in header:
                        buffer = buffer + column+","
                file.write(buffer[:-1])
                file.write(new_line)


		cursor.execute("select attribute, value,unit,date_value from gaap_map where eh_sk = "+str(eh_sk)+" and file_date_id = "+date_id+" and company_sk = "+str(company_sk)+" order by attribute, date_value desc")
		results = cursor.fetchall()
		found = 0	
		for result in results:
			attribute_col.append(result[0])
			value_col.append(result[1])
			date_value = result[3]
			try:
				if date_value.find("|;|") == -1:
					date_instant_col.append(date_value)
					date_start_col.append("")
					date_end_col.append("")
				else:
					date_instant_col.append("")
					date_start_col.append(date_value[:date_value.index("|;|")])
					date_end_col.append(date_value[date_value.index("|;|")+len("|;|"):])
			except:
					date_instant_col.append("")
					date_start_col.append("")
					date_end_col.append("")
			found = 1

		"""
		if found == 0:
			file.close()
			os.system('rm '+fn)
			return
		"""
			



		for index, attribute in enumerate(attribute_col):
			#file.write(attribute+"," +value_col[index]+"," +units_col[index]+"," +date_instant_col[index]+","+date_start_col[index]+","+date_end_col[index])
			# The NEW way to align with history
			file.write(attribute+"," +value_col[index]+"," +date_instant_col[index]+","+date_start_col[index]+","+date_end_col[index])
			
			file.write(new_line)

		file.close()
		if test == 0 and found == 1:
			#try:
			#	print "scp -i /home/peter/bin/testserver.pem "+fn+"   ubuntu@50.19.103.62:/master/parsed/"+date+'/'+symbol+"_"+form+"_"+period+".csv"
			#except:
			#	print "failed scp print"
			#os.system("scp -i /home/peter/bin/testserver.pem "+fn+"   ubuntu@50.19.103.62:/master/parsed/"+date+'/'+symbol+"_"+form+"_"+period+".csv")
			os.system("cp "+fn+"  /media/data/master/parsed/"+date+'/'+symbol+"_"+form+"_"+period+".csv")
			server_fn = form + "_"+symbol+"_"+period+".csv"
			server_fn = symbol+"_"+form+"_"+period+".csv"

                        try:
                                #s3.s3_load(fn,"parsed/"+fn[fn.rindex("/")+1:])
				# PMB FIX AFTER RELOAD
                                s3.s3_load(fn,"parsed/"+server_fn)
				pass
                        except:
				print "S3 load failed "
				print fn, "instrumental/"+fn[fn.rindex("/")+1:]

		else:
			if found == 1:
				os.system("cp "+fn+"  /media/data/master/parsed/"+date+'/'+symbol+"_"+form+"_"+period+".csv")



			
	
				

	# move me back after testing
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
        try:
                form = sys.argv[6]
        except:
                form = ""
        if form != "":
                fulfill_raw(date,test,email,form,company_sk,eh_sk,"","")
        else:
                #print date,test,email,"10-Q",company_sk
                fulfill_raw(date,test,email,"10-Q",company_sk,eh_sk,"","")
                fulfill_raw(date,test,email,"10-K",company_sk,eh_sk,"","")




	
