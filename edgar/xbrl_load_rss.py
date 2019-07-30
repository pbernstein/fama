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

def remove_dupes(seq):
   # not order preserving
   set = {}
   map(set.__setitem__, seq, [])
   return set.keys()


def file_get_contents(filename):
    with open(filename) as f:
        return f.read()




#def xbrl_load(file, company, cik, period, file_date):
def xbrl_load(file, cik, period, file_date):
	conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
	cursor = conn.cursor ()
	path = "/media/data/investments/data/edgar/forms/rss/land"
	loaded_path = "/media/data/investments/data/edgar/forms/rss/loaded" 
	error_path = "/media/data/investments/data/edgar/forms/rss/error" 
	error_canada_path = "/media/data/investments/data/edgar/forms/rss/error/canada" 
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
	context_labels = []
	context_values = []
	setting_units = 0
	unit_labels = []
	unit_values = []

	# Look for company info and look for context/unit labels

	for record in f:

		# Populate Company Info

		if record.find("COMPANY CONFORMED NAME:") != -1:
			company = "\""+record.split("\t").pop().replace("\n","").replace("\\","").replace("\&","\\&")+"\""
		if record.find("CENTRAL INDEX KEY:") != -1:
			cik = "\""+record.split("\t").pop().replace("\n","")+"\""
#		if record.find("STATE OF INCORPORATION:") != -1:
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
				#print record
				try:
					context_labels.append(record.split("\"")[1])
				except:
					context_labels.append(record.split("'")[1])

			if re.search("^.+ <xbrldi:explicitMember dimension", record) != None:
				context_labels[len(context_labels)-1] = "IGNORE ME"
				# If you see "explicitMember dimension", that means its a specific like: us-gaap:TreasuryStockMember
				# learn how to parse these later, for now ignore because they are creating dupes
	
			if re.search("^.+ <instant>", record) != None or record.find("<xbrli:instant") != -1:
				context_values.append(record.split(">")[1].split("<")[0])
			if re.search("^.+ <startDate>", record) != None or record.find("<xbrli:startDate") != -1:
				context_values.append(record.split(">")[1].split("<")[0])
			if re.search("^.+ <endDate>", record) != None or record.find("<xbrli:endDate") != -1:
				value = ""
				value = context_values[len(context_values)-1]  
				value = value +" - "+ record.split(">")[1].split("<")[0]
				context_values[len(context_values)-1] = value
			try:
				if record.find("</context>") != -1 or record.find("</xbrli:context>") != -1:
					setting_context = 0
				else:
					continue
			except:
				continue

		if record.find("Unit Section") != -1 or record.find("<xbrli:unit id=") != -1:
			setting_units = 1
			set_denom = 0

		if setting_units == 1:
                        if record.find("unit id=") != -1:
				try:
	                                unit_labels.append(record.split("\"")[1])
				except:
	                                unit_labels.append(record.split("'")[1])

                       	if re.search("^.+ <unitDenominator>", record) != None or record.find("<xbrli:unitDenominator>") != -1:
				set_denom = 1
                        if re.search("^.+ <measure>", record) != None or record.find("<xbrli:measure>") != -1:
				if set_denom == 1:
                                	unit_values[len(unit_values)-1] = unit_values[len(unit_values)-1] + "/"+ record.split("measure>")[1].split("<")[0].split(":")[1]
					set_denom = 0 
				else:
                                	unit_values.append(record.split("measure>")[1].split("<")[0].split(":")[1])
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

#		print industry
#		print cik
		# Populate gaap Values
		

		# Found my company/lookups, now lets look for gaap values

	f.close()
	f = open(file)	
#	print context_values
#	print context_labels

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
						
						## Swap out label for value
						try:
							set["date"] = context_values[context_labels.index(set["date"])]
						except:
							pass

						
						## Standardize values
						if set["date"].find("0.0.0") and (set["date"].find("as-of") or set["date"].find("from-")):
							set["date"] = set["date"].split(".")[0]

						if re.search("^c[0-9]", set["date"]) != None:
							set["date"] =  set["date"].split("_")[1].replace("c","")



                                        if element.find("unitRef") != -1:
                                                try:
                                                        set["units"] = "\""+element.split("=")[1].split("\"")[1]+"\""
                                                except: 
                                                        try:
                                                                set["units"] = "\""+element.split("=")[1].split("'")[1]+"\""
                                                        except: 
                                                                set["units"] = ""
                                                if set["units"] == "":  
                                                        set["units"] = "NULL"

						## Swap out label for value
						
						try:
							set["units"] = unit_values[unit_labels.index(set["units"].replace("\"",""))]
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

#	print attributes


#	cursor.execute(" select date_id from dates where date = \""+str("20120331")+"\"")
	cursor.execute(" select date_id from dates where date = \""+str(period)+"\"")
	row = cursor.fetchone()
	date_id = row[0]
	
	cursor.execute(" select date_id from dates where date = \""+str(file_date)+"\"")
	row = cursor.fetchone()
	file_date_id = row[0]

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
			shutil.move(file,error_canada_path+"/"+file[file.rindex("/")+1:].replace(".","__"+str(datetime.now()).replace(" ","_")+"."))
			return


	cursor.execute(" select company_sk from company where cik = "+str(cik))
	row = cursor.fetchone()
	company_sk = row[0]

	#
	# FUTURE, HANDLE ADDRESS UPDATES!
	#



	#print attributes
	inserts = 0
	error = 0 
	count = 0
	for element in attributes:
		#print "count = "+str(count)
		#count = count + 1
 		for a in element:
			if valid_dates.valid_dates.__contains__(a["date"]):
				#print "found a valid date:"+ a["field"] +": "+a["value"]
		#		print a["date"], a["field"] +": "+a["value"]
				inserts = inserts + 1
				try:
						value = a["value"].replace("\"","")
						value = float(value)
						#print "value = "+str(value)
						decimal = int(a["decimals"])
						#print "decimal = "+str(decimal)
						value = value * (10 ** decimal)
						#print "new value:"+str(value)
						value = "\""+str(value)+"\""
				except:
						pass
				try:
					cursor.execute ("insert into gaap_value (`company_sk`, `attribute`, `unit`, `value`, `date_id`, `file_date_id`) values ("+",".join(map(str,[company_sk, a["field"], a["units"], value , date_id, file_date_id]))+")")	
					#print "insert into gaap_value (`company_sk`, `attribute`, `unit`, `value`, `date_id`) values ("+",".join(map(str,[company_sk, a["field"], a["units"], value , date_id]))+")"

				except cursor.Error, e:
					try:
						e.args[1].find("Duplicate")
					except:
						print "Error %d: %s" % (e.args[0],e.args[1])
		 				print "Failed to insert gaap value: "+str(a)
						
			else:
	#			new_dates.append([a["date"],context_values[context_labels.index(a["date"])] ] )
				new_dates.append(a["date"])
		
	if inserts < 10:
		print "Only Inserted "+str(inserts)+" rows"
		print "Invalid dates:"
		unique_new_dates = remove_dupes(new_dates)
		for nd in unique_new_dates:
			if nd != "IGNORE ME":
				print nd 
		shutil.move(file,error_path+"/"+file[file.rindex("/")+1:].replace(".","__"+str(datetime.now()).replace(" ","_")+"."))	
	else:
		shutil.move(file,loaded_path+"/"+file[file.rindex("/")+1:].replace(".","__"+str(datetime.now()).replace(" ","_")+"."))	
	new_dates = []
		

	conn.commit()	
#	if count > 1:
#		break



	cursor.close()
	conn.commit()	
	conn.close()


		
