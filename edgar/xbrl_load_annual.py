#!/usr/bin/python
# xbrl_load_rss.py 


import sys
import re
import glob
import os
import shutil
import MySQLdb
from time import strptime
from datetime import datetime
import date_parse


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def remove_dupes(seq):
   # not order preserving
   set = {}
   map(set.__setitem__, seq, [])
   return set.keys()


def file_get_contents(filename):
    with open(filename) as f:
        return f.read()


def xbrl_load(file, company, cik, file_date):
	conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
	cursor = conn.cursor ()
	count = 0
	new_dates = []
	count = count + 1


	f = open(file)	
	result = ""
	attributes = []
	company = "\""+company+"\""
	cik = "\""+cik+"\""
	corp_state = ""
	industry = ""
	industry_id = ""
	address_line_1 = ""
	address_line_2 = ""
	city = ""
	state = "" 
	zip = "" 
	setting_context = 0
	context_values = {}
	context_counts = {}
	setting_units = 0
	unit_values = {}
	unit_ratio = [-1,-1]

	# Look for company info and look for context/unit labels

	for record in f:

		# Populate Company Info

		if record.find("COMPANY CONFORMED NAME:") != -1:
			company = "\""+record.split("\t").pop().replace("\n","").replace("\\","").replace("\&","\\&")+"\""
			#print "company = "+company," ", company[1]
		if record.find("CENTRAL INDEX KEY:") != -1:
			cik = "\""+record.split("\t").pop().replace("\n","")+"\""
		if re.search("^.+ STATE OF INCORPORATION:",record) != None:
			corp_state = "\""+record.split("\t").pop().replace("\n","")+"\""
		if record.find("STANDARD INDUSTRIAL CLASSIFICATION:") != -1:
			industry = "\""+record.split("\t").pop().split("[")[0].replace(","," ")+"\""
		if record.find("STANDARD INDUSTRIAL CLASSIFICATION:") != -1:
			industry_id = record.split("\t").pop().split("[")[1].replace("]","").replace("\n","")
		if record.find("STREET 1:") != -1 and address_line_1 == "":
			address_line_1 = "\""+record.split("\t").pop().replace("\n","").replace("\"","")+"\""
			address_line_1 = address_line_1.replace('""',"\"")
		if record.find("STREET 2:") != -1 and address_line_2 == "":
			address_line_2 = "\""+record.split("\t").pop().replace("\n","")+"\""
		if record.find("CITY:") != -1 and city == "":
			city = "\""+record.split("\t").pop().replace("\n","")+"\""
		if record.find("STATE:") != -1 and state == "":
			state = "\""+record.split("\t").pop().replace("\n","")+"\""
		if record.find("ZIP:") != -1 and zip == "":
			zip = "\""+record.split("\t").pop().replace("\n","")+"\""


		if record.find("<context id=") != -1 or record.find("<xbrli:context id=") != -1:	
			setting_context = 1

		if setting_context == 1:
			if record.find("context id=") != -1:
				try:
					context_label = record.split("\"")[1]
				except:
					context_label = record.split("'")[1]
	
			if record.find("<instant>") != -1 or record.find("<xbrli:instant") != -1:
				context_values[context_label] = record.split(">")[1].split("<")[0]
			 	context_counts[context_label] = 0	
		
			if record.find("<startDate>") != -1 or record.find("<xbrli:startDate") != -1:
				context_values[context_label] = record.split(">")[1].split("<")[0]
			 	context_counts[context_label] = 0	

			if record.find("<endDate>") != -1 or record.find("<xbrli:endDate") != -1:
				context_values[context_label] = record.split(">")[1].split("<")[0]
			try:
				if record.find("</context>") != -1 or record.find("</xbrli:context>") != -1:
					setting_context = 0
				else:
					continue
			except:
				continue

		if record.find("Unit Section") != -1 or record.find("<xbrli:unit id=") != -1 or record.find("<unit id=") != -1:	
			setting_units = 1
			set_denom = 0
			set_numer = 0

		if setting_units == 1:
                        if record.find("unit id=") != -1:
				try:
	                                unit_label = record.split("\"")[1]
				except:
	                                unit_label = record.split("'")[1]

                       	if record.find("unitDenominator>") != -1 and record.find("/") == -1:
				set_denom = 1
                       	if record.find("unitNumerator>") != -1 and record.find("/") == -1:
				set_numer = 1
                        if record.find("measure>") != -1:
				if set_numer == 1:
					try:
						unit_ratio[0] = record.split("measure>")[1].split("<")[0].split(":")[1]
					except:
						unit_ratio[0] = record.split("measure>")[1].split("<")[0]
					set_numer = 0
				elif set_denom == 1:
					try:
						unit_ratio[1] = record.split("measure>")[1].split("<")[0].split(":")[1]
					except:
						unit_ratio[1] = record.split("measure>")[1].split("<")[0]
						
					set_denom = 0
				else:
					try:
	                                	unit_values[unit_label] = record.split("measure>")[1].split("<")[0].split(":")[1]
					except:
	                                	unit_values[unit_label] = record.split("measure>")[1].split("<")[0]
			
			if unit_ratio[0] != 1 and unit_ratio[1] != -1:
                                	unit_values[unit_label] = str(unit_ratio[0]) +"/"+str(unit_ratio[1])
					unit_ratio[0] = -1
					unit_ratio[1] = -1
                        try:
				if record.find("</unit>") != -1 or record.find("</xbrli:unit>") != -1:
                                        setting_units = 0
                                else:
	                        	continue
			except:
	                        continue
			
			

		if address_line_2 == "":
			address_line_2 = "NULL";	
		
		if corp_state == "":
			corp_state = "NULL";	
	
		if industry  == "":
			industry = "NULL";	
			industry_id = "NULL";	
		

		if city  == "":
			city = "NULL";	
		
		if state  == "":
			state = "NULL";	

		if zip  == "":
			zip = "NULL";	



		# Found my company/lookups, now lets look for gaap values

	f.close()
	f = open(file)	
	for record in f:
		line = []
		try:
				record.index("<us-gaap:")
				set = {}
				set["field"] = ""
				set["value"] = ""
				set["date"] = ""
				set["units"] = "NULL"
				set["decimals"] = "NULL"

				for element in record.split(" "):
                                        if element.find("<us-gaap") != -1:
                                                try:
                                                        set["field"] = "\""+element.split(":")[1]+"\""
                                                except:
                                                        print "Can't set field name!"
                                                        exit(1)

                                        if element.find("contextRef") != -1:
                                                try:
                                                        set["date"] = element.split("=")[1].split("\"")[1]

                                                except:
                                                        try:
                                                                set["date"] = element.split("=")[1].split("'")[1]
                                                        except: 
                                                                set["date"] = ""
                                                if set["date"] == "":  
                                                        set["date"] = ""
						
						try:
							context_counts[set["date"]] = context_counts[set["date"]] + 1	
						except:
							pass


                                        if element.find("unitRef") != -1:
                                                try:
                                                        #set["units"] = "\""+element.split("=")[1].split("\"")[1]+"\""
                                                        set["units"] = element.split("=")[1].split("\"")[1]
                                                except: 
                                                        try:
                                                                #set["units"] = "\""+element.split("=")[1].split("'")[1]+"\""
                                                                set["units"] = element.split("=")[1].split("'")[1]
                                                        except: 
                                                                set["units"] = ""
                                                if set["units"] == "":  
                                                        set["units"] = "NULL"

						
						## Swap out label for value
						
						try:
							set["units"] = unit_values[set["units"]].replace("\"","")
		
							set["units"] = "\""+set["units"]+"\""

						except:
							pass
						
			
					## Standardize Unit values

					if set["units"].find("iso") != -1:
						if set["units"].find("_") != -1:
							set["units"] = "\""+set["units"].split("_")[1]				
						if set["units"].find(":") != -1:
							set["units"] = "\""+set["units"].split(":")[1]				

                                        if element.find("decimals") != -1:
                                                try:
                                                        set["decimals"] = element.split("=")[1].split("\"")[1]
                                                except: 
                                                        try:
                                                                set["decimals"] = element.split("=")[1].split("'")[1]
                                                        except: 
                                                                set["decimals"] = ""
                                                if set["decimals"] == "":  
                                                        set["decimals"] = "NULL"

					if element.find(">") != -1:
						set["value"] = "\""+element[element.index(">")+1:element.index("<")]+"\""

				if set != {}:
					line.append(set)
				attributes.append(line)

		except: 
				#continue
				pass

	f.close()

	cursor.execute(" select date_id from dates where date = \""+str(file_date)+"\"")
	row = cursor.fetchone()
	file_date_id = row[0]

	candidate, period = date_parse.get_period(file_date_id, context_values, context_counts)
	if candidate == "RETURN 1":
		return 1
	if candidate == "INVALID FORMAT":
		return 1
	if candidate == "FAIL":
		return 1

	print "candidate = "+candidate
	
	for i in period:
		if period[i] == "20111231":
			print i, context_values[i], period[i]
	
	exit(0)




	#cursor.execute(" select date_id from dates where date = \""+str(candidate)+"\"")
	#row = cursor.fetchone()
	#date_id = row[0]

	

	print "Company: "+company

	name = ""
	cursor.execute(" select name from company where cik = "+str(cik))
	row = cursor.fetchone()

	try:
		name = row[0]
		
		if name != None and name != company.replace("\"",""): 
			print "10q and DB have a CIK/company name mismatch!!!" 
			print "10Q:"+ name 
			print "DB:"+ company 
	except:
		try:
			cursor.execute ("insert into company (`name`, `cik`, `industry`, `industry_id`, `corp_state`, `address_line_1`, `address_line_2`, `city`, `state`, `zip`) values ("+",".join(map(str,[company, cik, industry, industry_id, corp_state, address_line_1, address_line_2, city, state, zip]))+")")
		except cursor.Error, e:
			try:
				e.args[1].find("Duplicate")
			except:
				print "Error %d: %s" % (e.args[0],e.args[1])
				print "failed to insert company info: "+",".join(map(str,[company, cik, industry, industry_id, corp_state, address_line_1, address_line_2, city, state, zip]))
			#shutil.move(file,error_canada_path+"/"+file[file.rindex("/")+1:].replace(".","__"+str(datetime.now()).replace(" ","_")+"."))
			return 2


	cursor.execute(" select company_sk from company where cik = "+str(cik))
	row = cursor.fetchone()
	company_sk = row[0]

	#
	# FUTURE, HANDLE ADDRESS UPDATES!
	#


	#
	# FUTURE, HANDLE ATTRIBUTE UPDATES, this is going to happen
	#



	# Create element_dict
	# Only insert rows that are from the candidate quarter , don't insert any rows where I have multiple values for that
	# attribute for the candidate quarter
	#	

	"""
	element_dict = {}
	for element in attributes:
		for a in element:
				try:
					if period[str(a["date"])] == candidate:
						try:
							element_dict[a["field"]] = element_dict[a["field"]] + 1
						except:
							element_dict[a["field"]] = 1
				except:
					pass

	"""
		
	inserts = 0
	error = 0 
	count = 0
	for element in attributes:
 		for a in element:
			try:
				if period[str(a["date"])] == candidate and element_dict[a["field"]] == 1:
					inserts = inserts + 1
					try:
							value = a["value"].replace("\"","")
							value = "\""+str(value)+"\""
					except:
							pass
					try:
						
						cursor.execute ("insert into gaap_value (`company_sk`, `attribute`, `unit`, `value`, `date_id`, `file_date_id`) values ("+",".join(map(str,[company_sk, a["field"], a["units"], value , date_id, file_date_id]))+")")	
						conn.commit()	
						#print "insert into gaap_value (`company_sk`, `attribute`, `unit`, `value`, `date_id`, `file_date_id`) values ("+",".join(map(str,[company_sk, a["field"], a["units"], value , date_id, file_date_id]))+")"

					except cursor.Error, e:
						try:
							e.args[1].find("Duplicate")
							#print "Error %d: %s" % (e.args[0],e.args[1])
							#print "insert into gaap_value (`company_sk`, `attribute`, `unit`, `value`, `date_id`, `file_date_id`) values ("+",".join(map(str,[company_sk, a["field"], a["units"], value , date_id, file_date_id]))+");"
			
						except:
							print "Error %d: %s" % (e.args[0],e.args[1])
							print "Failed to insert gaap value: "+str(a)
							
				else:
					new_dates.append(a["date"])
			except:
				print "a[date]  = "+str(a["date"])
				print "peroid = "+str(period)
				print "a[field] = "+str(a["field"])
				print "element = "+str(element_dict) # its not in element dict
				
		
	if inserts < 10:
		print "Only Inserted "+str(inserts)+" rows"
		print "Invalid dates:"
		unique_new_dates = remove_dupes(new_dates)
		for nd in unique_new_dates:
			if nd != "IGNORE ME":
				print nd +" | "+ str(context_counts[nd])
		return 1
	else:
		return 0
	new_dates = []
		

#	if count > 1:
#		break



	cursor.close()
	conn.commit()	
	conn.close()


	
if __name__ == '__main__':
	file = sys.argv[1]
	company = sys.argv[2]
	cik = sys.argv[3]
	file_date = sys.argv[4]
	xbrl_load(file, company, cik, file_date)
