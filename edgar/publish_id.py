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


def fulfill(date,test,email,form_type,company_sk,eh_sk):
	
	conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape") 
	cursor = conn.cursor ()

	form = form_type

	#print " in fulfill with "+date, email, form_type, str(company_sk)

	cursor.execute("select date_id from dates where date = \""+date+"\"") 
	date_id = str(cursor.fetchone()[0])


	company = []
	
	cursor.execute("select c.cik, c.name  from company c,  (select company_sk from gaap_value where file_date_id = "+date_id+" group by company_sk) cs, extract_history eh  where c.company_sk = "+str(company_sk)+" and c.company_sk = cs.company_sk and c.cik = eh.cik and eh.date_id >= "+date_id+" and eh.form = \""+form_type+"\"  and eh.eh_sk = "+str(eh_sk)+" order by name")

	result = cursor.fetchall()
	company.append([result[0], result[1]])


	cik = company[0]
	company_name = company[1]
	company_name = company_name.replace(" ","_").replace("/","-").replace(".","").replace("&","AND").replace(",","")
	print "Fulfilling Company :"+company_name

	num_companies = "1"
	print "num companies in fulfill_id = "+num_companies

	if test == 0:
		os.system('ssh -i ~/bin/testserver.pem ubuntu@50.19.103.62 "mkdir -p /master/instrumental/'+date+'"')

	count = 0 

	cursor.execute("select period from gaap_value where eh_sk = "+str(eh_sk)+" and file_date_id = "+str(date_id)+" and company_sk = "+str(company_sk)+" limit 1")

	try:
		period = cursor.fetchone()[0]
	except:
		try:
			cursor.execute("select period from gaap_value where file_date_id = "+str(date_id)+" and company_sk = "+str(company_sk)+" limit 1")
			period = cursor.fetchone()[0]
		except: 
			print "period lookup failed! "
			return(0)
	

	# Set header ( same for each filing )

	header = []
	header.append("Attribute")
	header.append("Value")
	header.append("Date:Instant")
	header.append("Date:RangeStart")
	header.append("Date:RangeEnd")

	# Fulfill!


        attribute_col = []
        value_col = []
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

        #print "select attribute, value, date_instant, date_start, date_end from ins_value, iset is where is.attribute = attribute and date_id = "+str(date_id)+" and company_sk = "+str(company_sk)+" order by iset.priority"
        cursor.execute("select iv.attribute, iv.value, iv.date_instant, iv.date_start, iv.date_end from ins_value iv, iset ise where iv.form = "+form+" and ise.i_attribute = iv.attribute and iv.date_id = "+str(date_id)+" and iv.company_sk = "+str(company_sk)+" order by ise.priority")
        results = cursor.fetchall()
        for result in results:
                attribute = result[0]
                value = result[1]
                date_instant = result[2]
                date_start = result[3]
                date_end = result[4]

                cursor.execute("select value, date_instant, date_start, date_end from ins_modify where date_id = "+str(date_id)+" and company_sk = "+str(company_sk)+" and form = \""+form+"\" and attribute = \""+attribute+"\"")
                result = cursor.fetchone()
                try:
                        value = result[0]
                        date_instant = result[1]
                        date_start = result[2]
                        date_end = result[3]
                except:
                        pass


                attribute_col.append(attribute)
                value_col.append(value)
                date_instant_col.append(date_instant)
                date_start_col.append(date_start)
                date_end_col.append(date_end)



        os.system('mkdir -p /media/data/investments/data/edgar/fulfillment/instrumental/'+date)
        os.system('ssh -i ~/bin/testserver.pem ubuntu@50.19.103.62 "mkdir -p /master/html/'+date+'"')
        fn = "/media/data/investments/data/edgar/fulfillment/instrumental/"+date+"/"+company_name+"_instrumental_"+form+"_"+date+".csv"

        print "writing: "+fn

        file = open(fn,'w')
        new_line = "\r\n" # Windows
        #new_line = "\n" # Linux
        buffer = ""
        for column in header:
                buffer = buffer + column+","
        file.write(buffer[:-1])
        file.write(new_line)



        for index, attribute in enumerate(attribute_col):
                #print attribute
                #print value_col[index]
                #print date_instant_col[index]
                #print date_start_col[index]
                #print date_end_col[index]
                file.write(attribute+","+value_col[index]+","+date_instant_col[index]+","+date_start_col[index]+","+date_end_col[index])
                file.write(new_line)


        file.close()

        #os.system("scp -i ~/bin/testserver.pem "+fn+"   ubuntu@50.19.103.62:/master/instrumental/"+date)



	

	cursor.close()
	conn.commit()	
	conn.close()


