#!/usr/bin/python


import sys
import re
import glob
import os
import publish_s3 as s3

import MySQLdb
import buckets
import time
from time import strptime
import shutil
import send_generic_email_attachment as send_email
import parsed_tweet


def dprint(self,debug):
	if debug == 1:
		print self


def find_value(cursor, eh_sk, attribute):
        try:
                #print 'select value from ins_value where eh_sk = '+str(eh_sk)+' and attribute = "'+attribute+"\""
                cursor.execute('select value from ins_value where eh_sk = '+str(eh_sk)+' and attribute = "'+attribute+"\"")
                return str(cursor.fetchone()[0])
        except:
                print "tweeting died in select"
                return "fail"

def find_prev_value(cursor, eh_sk, attribute):
        try:
                cursor.execute('select company_sk, form from ins_value where eh_sk = '+str(eh_sk)+' and attribute = "'+attribute+"\"")
                result =  cursor.fetchone()
                company_sk =  str(result[0])
                form =  str(result[1])
                cursor.execute('select value, form from ins_value where company_sk = '+str(company_sk)+' and attribute = "'+attribute+"\" order by ins_sk desc limit 2")
                results = cursor.fetchall()
                try:
                    pre_value = str(results[1][0])
                    pre_form = str(results[1][1])
                    if pre_form != form:
                        pre_value = -1
                except:
                    pre_value = -1

                if pre_value == -1:
                        return "fail"
                else:
                        return pre_value

        except:
                print "finding the previous value in find_prev_value failed"
                return "fail"



def ins_tweet(cursor,symbol, eh_sk):
	print "in ins_tweet"
        try:

            attributes = {"Revenues":"Revenues","Cash":"Cash","Assets":"Assets","NetIncome":"Net Income","AdditionalPaidInCapital":"Additional Paid In Capital","AccountsReceivable":"Accounts Receivable","AccountsPayable":"Accounts Payable"}
	    at_list = sorted(attributes.keys())

            """
            num_elements = len(at_list)
            counter = open('/tmp/counter',"r+")
            for row in counter:
			count = row.split("\n")[0]
            counter.seek(0)
            counter.write(str(int(count) + 1))
            counter.close()


            next_at = int(count) % num_elements
            for i in range(next_at):
                at_list.append(at_list.pop(0))

                    for key in at_list:
                print "key = "+key
                            value = find_value(cursor,eh_sk,key)
                print "value = "+value
                            if value != "0" and value != "NR" and value != "fail":
                                    print symbol, attributes[key], value
                                    tweeted = parsed_tweet.tweet(symbol, attributes[key], value)
                    #print "return code: "+str(tweeted)
                                    if tweeted == 1:
                                            return
            """

            key = 'Revenues'
            value = find_value(cursor,eh_sk,key)
            try:
                prev_value = find_prev_value(cursor,eh_sk,key)
            except:
                prev_value = "fail"
            print "value = "+value
            if prev_value != "fail":
            	print "prev value = "+prev_value
                if value != "0" and value != "NR" and value != "fail":
                        print symbol, attributes[key], value
                        tweeted = parsed_tweet.compare_tweet(symbol, attributes[key], value,prev_value)
                else:
                        print "Bad compare tweet!"
            else:
                if value != "0" and value != "NR" and value != "fail":
                        print symbol, attributes[key], value
                        tweeted = parsed_tweet.tweet(symbol, attributes[key], value)
                else:
                        print "Bad parsed tweet!"


        except:
                print "tweeting died in tweet"



#def fulfill(date,test,email,form_type,company_sk,eh_sk,dir,fn):
def fulfill(date,form_type,company_sk,eh_sk):
	test = 0
	email = 0
	dir = ""
	fn =  ""

	conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
	cursor = conn.cursor ()

	debug = test
	form = form_type.replace("/","-").replace("'","-").replace('"',"-")

	#print " in fulfill_id with "+date, email, form_type, str(company_sk)
	print "fulfill id called as "
	print "fulfill("+date,test,email,form,company_sk,eh_sk
	print

	cursor.execute("select date_id from dates where date = \""+date+"\"")
	date_id = str(cursor.fetchone()[0])


	# Find Instrumental Set Attributes

	attributes = []
	num_dates = {}
	gaap_date_value = {}
	column_dict = {}
	attribute_col = []
	cursor.execute("select i_attribute, num_dates from iset order by priority")
	results = cursor.fetchall()
	for result in results:
		attributes.append(result[0])
		num_dates[result[0]] = result[1]

	for a in attributes:
		cursor.execute("select filing_attribute, source, type from imap where i_attribute = \""+a+"\"  and source = \"x\" order by priority")
		results = cursor.fetchall()
		column_dict[a] = []
		for result in  results:
			column_dict[a].append(result[0])

	columns = column_dict


	# Find Companies that filed today

	companies = []
	#print "finding companies"
        print "select c.cik, c.name, c.company_sk from company c,  (select company_sk from gaap_value where file_date_id = "+date_id+" group by company_sk) cs, extract_history eh  where c.company_sk = "+str(company_sk)+" and c.company_sk = cs.company_sk and cast(c.cik as unsigned) = cast(eh.cik as unsigned) and eh.date_id >= "+date_id+" and eh.form = \""+form_type+"\"  and eh.eh_sk = "+str(eh_sk)+" order by name"
        cursor.execute("select c.cik, c.name, c.company_sk from company c,  (select company_sk from gaap_value where file_date_id = "+date_id+" group by company_sk) cs, extract_history eh  where c.company_sk = "+str(company_sk)+" and c.company_sk = cs.company_sk and cast(c.cik as unsigned) = cast(eh.cik as unsigned) and eh.date_id >= "+date_id+" and eh.form = \""+form_type+"\"  and eh.eh_sk = "+str(eh_sk)+" order by name")


	results = cursor.fetchall()
	for result in results:
		companies.append([result[0], result[1]])

	num_companies = str(len(companies))
	#print "num companies in fulfill_id = "+num_companies
	"""
	if test == 0 and len(companies) > 0:
		os.system('ssh -i ~/bin/testserver.pem ubuntu@50.19.103.62 "mkdir -p /master/instrumental/'+date+'"')
	if test == 1:
		os.system('mkdir -p /media/data/id/refulfill/instrumental/'+date)
	"""

	count = 0

	# Set header ( same for each filing )

	header = []
	header.append("Attribute")
	header.append("Value")
	header.append("Date:Instant")
	header.append("Date:RangeStart")
	header.append("Date:RangeEnd")

	# Fulfill!

	for company in companies:
		cik = company[0]
		company_name = company[1]
		company_name = company_name.replace(" ","_").replace("/","-").replace(".","").replace("&","AND").replace(",","").replace("(","").replace(")","").replace('"','').replace("'","").upper()



		output = []

		attribute_col = []
		value_col = []
		date_instant_col = []
		date_start_col = []
		date_end_col = []

		attribute_col.append("Company Name")
		value_col.append(company_name.replace("_"," "))
		date_instant_col.append(date)
		date_start_col.append("")
		date_end_col.append("")

		attribute_col.append("Company Key")
		value_col.append(str(int(cik)))
		date_instant_col.append("")
		date_start_col.append("")
		date_end_col.append("")




		#cursor.execute("select exchange, symbol from symbol where current = 1 and cik = \""+str(cik)+"\" order by exchange desc, length(symbol)  limit 1") # <- code a better rule than this
		cursor.execute("select exchange, symbol from symbol where "+str(date_id)+" > start_date_id and "+str(date_id)+" < end_date_id and cik != 'FAILURE' and cast(cik as unsigned) = \""+str(int(cik))+"\" order by exchange desc, length(symbol)  limit 1")

		result = cursor.fetchone()
		try:
			exchange = result[0]
			symbol = result[1]
		except:
			exchange = "MISSING"
			symbol = "MISSING"
			print "no symbol found for "+company_name
			continue # TAKE THIS OUT TO FULFILL RECORDS WITH MISSING SYMBOLS


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

		#print "select period from gaap_value where eh_sk = "+str(eh_sk)+" and file_date_id = "+str(date_id)+" and company_sk = "+str(company_sk)+" limit 1"
		cursor.execute("select period from gaap_value where eh_sk = "+str(eh_sk)+" and file_date_id = "+str(date_id)+" and company_sk = "+str(company_sk)+" limit 1")




		try:
			period = cursor.fetchone()[0]
		except:
			try:
				cursor.execute("select period from gaap_value where file_date_id = "+str(date_id)+" and company_sk = "+str(company_sk)+" limit 1")
				period = cursor.fetchone()[0]
			except:
				print "period lookup failed! "
				continue





		id = {}
		id_order = []
		column_used = {}

		for attribute in attributes:
			try:
				value = "NR"
				gaap_date_value[attribute] = ""
				id_order.append(attribute)
				id[attribute] = str(value)
				column_used[attribute] = ""


				for a in columns[attribute]:
					element = {}
                                        cursor.execute("select value,date_value from gaap_value where company_sk = "+str(company_sk)+" and UPPER(substring_index(attribute,\"_\",1)) = \""+a.upper()+"\" and eh_sk = "+str(eh_sk)+" and file_date_id = "+str(date_id)+" and new_info = 1 order by length(attribute)")

					try:
						result = cursor.fetchone()
						if num_dates[attribute] == 2:
							if result[1].find("|;|") != -1:  # My delimiter between dates, if this is present, there are two dates
								value = result[0]
								gaap_date_value[attribute] = result[1]
						if num_dates[attribute] == 1:
							if result[1].find("|;|") == -1:  # My delimiter between dates, if this is not present, there is one date
								value = result[0]
								gaap_date_value[attribute] = result[1]

						#dprint("assigning id["+a+"] = "+str(value),debug)
						if value != "NR":
							id[attribute] = str(value)
							column_used[attribute] = a
							#dprint(a+": "+ str(value),debug)
							break
					except:
						#print "Can't parse value"
						#pass
						#id[attribute] = 0
						continue

					count = count + 1
			except:
				pass


		for attribute in id_order:
			try:
				if column_used[attribute].upper() == "LiabilitiesAndStockholdersEquity".upper():
					id[attribute] = str(int(id[attribute]) - int(id["StockholdersEquity"]))
			except:
				pass


		## Fix Current Liabilities

		for attribute in id_order:
			try:
				if attribute == "LiabilitiesCurrent" and str(id[attribute]) == "NR":
					id[attribute] = id["Liabilities"]
					gaap_date_value[attribute] = gaap_date_value["Liabilities"]
			except:
				pass

		for attribute in id_order:
			try:
				if attribute == "AssetsCurrent" and str(id[attribute]) == "NR":
					id[attribute] = id["Assets"]
					gaap_date_value[attribute] = gaap_date_value["Assets"]
			except:
				pass


		attribute_col.append("Quarter Filed")
		value_col.append(period)
		date_instant_col.append(date)
		date_start_col.append("")
		date_end_col.append("")

		#print "deleting from ins_value"
		cursor.execute("delete from ins_value where company_sk = "+str(company_sk)+" and period = \""+period+"\" and form = \""+form+"\" and eh_sk = "+str(eh_sk))
		for attribute in id_order:
			try:
				attribute_col.append(attribute)
				value_col.append(id[attribute])
				try:
					if num_dates[attribute] == 1:
						date_instant_col.append(gaap_date_value[attribute])
						date_instant = gaap_date_value[attribute]
						date_start = ""
						date_end = ""
						date_start_col.append("")
						date_end_col.append("")
					else:
						date_instant_col.append("")
						date_start_col.append(gaap_date_value[attribute][:gaap_date_value[attribute].index("|;|")])
						date_end_col.append(gaap_date_value[attribute][gaap_date_value[attribute].index("|;|")+len("|;|"):])
						date_instant = ""
						date_start = gaap_date_value[attribute][:gaap_date_value[attribute].index("|;|")]
						date_end = gaap_date_value[attribute][gaap_date_value[attribute].index("|;|")+len("|;|"):]
				except:
						date_instant_col.append("")
						date_start_col.append("")
						date_end_col.append("")
						date_instant = ""
						date_start = ""
						date_end = ""



				try:
					cursor.execute("insert into ins_value (company_sk, attribute, date_id, value, date_instant, date_start, date_end, period,form, eh_sk) values ("+str(company_sk)+",\""+attribute+"\","+date_id+",\""+id[attribute]+"\",\""+date_instant+"\",\""+date_start+"\",\""+date_end+"\",\""+period+"\",\""+form+"\","+str(eh_sk)+")")
				except:
					print "could not insert:"

					if attribute == "Revenues":
						pass
						#parsed_tweet.tweet(symbol, attribute, value)

			except:
				#value_col.append("")
				pass

		if symbol != "MISSING":
			try:
				#print " ins_tweet("+str(cursor),symbol, eh_sk
				ins_tweet(cursor,symbol, eh_sk)
			except:
				print "ins_tweet function died"




	cursor.close()
	conn.commit()
	conn.close()
	return(num_companies)





if __name__ == '__main__':
        date = sys.argv[1]
	form_type = sys.argv[2]
	company_sk = sys.argv[3]
	eh_sk = sys.argv[4]
	#fulfill(date,test,email,form,company_sk,eh_sk,"","")
	fulfill(date,form_type,company_sk,eh_sk)



