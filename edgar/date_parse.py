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

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start



def padd_single_digit_dates(value):
	# Turns "1-1-2012" into "01-01-2012"
	buffer = value
	value_len = len(value)
	#print "value = "+value
	for i, v in enumerate(value):
		if i < 1 or i == (value_len - 2):
			if not unicode(value[i-1]).isnumeric()  and unicode(v).isnumeric and not unicode(value[i+1]).isnumeric():
				buffer[i-1] = "0"
	if unicode(value[0]).isnumeric and not unicode(value[1]).isnumeric():
		buffer = "0"+buffer

	return buffer


def parse_numeric(date,YYYY_index):
	return([date[4:6],date[6:8]])



def get_period(file_date_id, form, context_values, context_counts):
	period = {}

	#print "in get_period with form = "+form

	# file_date_id is the date_id that this document was filed with the SEC
	# context_values is a dict that looks like {'label':'value', 'label':'value',...}
	# context_counts is a dict that looks like {'label':# of times label appears, 'label':# of times label appears',...}



        conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
        cursor = conn.cursor ()

	"""
	Hygiene:
	Convert all "single digit format" ("1_6_2011") to zero filled ("01_06_2011")
	Remove seperators ("01_06_2011") to ("01062011")
	"""

	quarter_dict = {1:"0331",2:"0630",3:"0930",4:"1231"}
	month_list = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
	year_list = ["1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001","2002","2003","2004","2005","2006","2007","2008","2009","2010", "2011", "2012", "2013", "2014"]
	abbrev_year_list = ["90","91","92","93","94","95","96","97","98","99","00","01","02","03","04","05","06","07","08","09","10", "11", "12", "13","14"]


	# Build a dict of the date_id's for the end of each supported quarter

	date_id_dict = {}
	period_quarter_map = {}
	for year in year_list:
		for quarter in quarter_dict:
				date = str(year)+str(quarter_dict[quarter])
			        cursor.execute(" select date_id from dates where date = \""+str(date)+"\"")
			        row = cursor.fetchone()
			        date_id_dict[date] = row[0]

				#date = date[:4]+"-"+date[4:6]+"-"+date[6:]
				period_quarter_map[date] = year + "Q"+str(quarter)

        cursor.close()
        conn.commit()
        conn.close()

		

	# Build the period dict

	# Walk through all of the labels:

	for label in context_values:
		value = context_values[label]
		month_index = []
		year_index = []
		year_label_index = []
		quarter_label_index = []
		MM = "unknown"
		QQ = "unknown"
		start_mm = "unknown"
		end_mm = "unknown"
		quarter = "unknown"
		quarter_LABEL = "unknown"
		format = "unknown"
		YYYY = "unknown"
		start_YYYY = "unknown"
		end_YYYY = "unknown"
		YYYY_LABEL = "unknown"
		start_YYYY_LABEL = "unknown"
		end_YYYY_LABEL = "unknown"
		YYYY_index = -1
		ABCD = "unknown"
	
		#if label == 'c4_From1Jan2012To30Sep2012':
		#	print ""
		#	print "value =  "+value	
		#	print "label = "+label

		if value.find("|;|") != -1:
			# I AM TWO DATES

			# Two dates!
			#print "Found two dates!"
			start_date = value[:value.index("|;|")]
			end_date = value[value.index("|;|")+3:]

			try:	
				start_YYYY = start_date[start_date.index("20"):start_date.index("20")+4]
				end_YYYY = end_date[end_date.index("20"):end_date.index("20")+4]
			except:
				#print "could not find year for:"
				#print value
				period[label] =  "INVALID FORMAT in two dates"
				#print "bailing on the two date thing, couldn't find a year for :"+ value
				continue

                        ###
                        # Convert all "single digit format" ("1_6_2011") to zero filled ("01_06_2011")
                        ###
                        try:   
                                start_date = padd_single_digit_dates(start_date)
                                end_date = padd_single_digit_dates(end_date)
                        except:
				print "Could not padd single digits for this date!  value = |"+value+"| label = "+label
				period[label] =  "INVALID FORMAT in padd single digits"
				continue
				# return ["RETURN 1","RETURN 1"]



                        ###
                        #  Remove all non alpha numerics
                        ###
			
			start_date =  re.sub(r'\W+', '', start_date)
			start_date =  re.sub(r'_+', '', start_date)
			start_date =  re.sub(r'-+', '', start_date)
			end_date =  re.sub(r'\W+', '', end_date)
			end_date =  re.sub(r'_+', '', end_date)
			end_date =  re.sub(r'-+', '', end_date)

                        #print "Label "+ label +" Hygiene value:"+start_date, end_date


                        try:
				#print "parsing value :"+value
                                result = parse_numeric(start_date,start_date.index(start_YYYY))
                                start_mm = result[0]
                                start_dd = result[1]
                                result = parse_numeric(end_date,end_date.index(end_YYYY))
                                end_mm = result[0]
                                end_dd = result[1]
				#print "got "+start_mm, start_dd, end_mm, end_dd
                        except:
				#if value != "":
				#	print "Failed to parse_numeric: "+value
			#	print "Failed to parse_numeric: "+value
				period[label] = "INVALID FORMAT in start end assignment, value = |"+value,str(start_YYYY),str(end_YYYY)
				continue

			"""
			print "start_YYYY = "+start_YYYY
			print "start_mm = "+start_mm
			print "end_YYYY = "+end_YYYY
			print "end_mm = "+end_mm
			"""
	
			# Confirm I am in a good place
			if start_YYYY == "unknown":
				print "YYYY = "+YYYY+" and MM = "+MM
				print "what the hell am i? ", value
				continue

			if form == "10-Q":
				if end_mm in ["02","03","04"] and start_mm in ["11", "12","01","02"]: 
					QQ = quarter_dict[1]
				if end_mm in ["05","06","07"] and start_mm in ["02", "03","04","05"]: 
					QQ = quarter_dict[2]
				if end_mm in ["08","09","10"] and start_mm in ["05", "06","07","08"]: 
					QQ = quarter_dict[3]
				if end_mm in ["11","12"] and start_mm in ["08", "09","10","11"]: 
					QQ = quarter_dict[4]
				if end_mm == "01":
					QQ = quarter_dict[4]
					###
					#	This means it is a January of 201N, but filing is really about the last quarter of 201(N-1).  Do the needful!
					###
					end_YYYY = str(int(end_YYYY)-1)

			elif form == "10-K":
				if end_mm in ["02","03","04"] and start_mm in ["02","03","04"]:
					QQ = quarter_dict[1]
				if end_mm in ["05","06","07"] and start_mm in ["05","06","07"]:
					QQ = quarter_dict[2]
				if end_mm in ["08","09","10"] and start_mm in ["08","09","10"]:
					QQ = quarter_dict[3]
				if end_mm in ["11","12"] and start_mm in ["11","12"]:
					QQ = quarter_dict[4]
				if end_mm == "01":
					QQ = quarter_dict[4]
					###
					#	This means it is a January of 201N, but filing is really about the last quarter of 201(N-1).  Do the needful!
					###
					end_YYYY = str(int(end_YYYY)-1)

			else:
				print "Received FORM = "+form
				print "date_parse"
				print "I don't know what to do with this!"
				period[label] = "NOT A QUARTER"
				
			if QQ != "unknown":	
				#print "5 classifying label "+label+" with value "+value+" as "+YYYY+QQ+" with MM "+MM+" with ABCD = "+ABCD+" and format "+format
				period[label] = end_YYYY+QQ
			else:
				#print "bailing on two dates, I am not a quarter"
				#print "Couldn't assign: "+str(label)
				#print "start_mm: "+str(start_mm)
				#print "end_mm: "+str(end_mm)
				#print "value: "+str(value)
                                period[label] =  "INVALID FORMAT"
				#break
				continue


			#print "period = "+str(period[label])

		else:
			# I AM ONE DATE
			try:
				YYYY = value[value.index("20"):value.index("20")+4]
		        except: 
                                #print "could not find year for:"
                                #print value
                                period[label] =  "INVALID FORMAT in one date"
                                continue


			try:
                       		value = padd_single_digit_dates(value)
                        except:
				print "Could not padd single digits for this date!  value = |"+value+"| label = "+label
				period[label] =  "INVALID FORMAT"
				continue
				# return ["RETURN 1","RETURN 1"]
              
			value =  re.sub(r'\W+', '', value)
			value =  re.sub(r'_+', '', value)
			try:
				result =  parse_numeric(value,YYYY_index)
				MM = result[0]
				DD = result[1]
			except:
				period[label] = "INVALID FORMAT"
				continue

					
			#print "YYYY "+YYYY
			#print "MM = "+MM

			# Confirm I am in a good place
			if YYYY == "unknown" or MM == "unknown":	
				print "YYYY = "+YYYY+" and MM = "+MM
				print "what the hell am i? ", value
				continue
				#return(["FAIL","FAIL"])
				#exit(1)

			if MM in ["02","03","04"]: 
				QQ = quarter_dict[1]
			if MM in ["05","06","07"]: 
				QQ = quarter_dict[2]
			if MM in ["08","09","10"]: 
				QQ = quarter_dict[3]
			if MM in ["11","12"]: 
				QQ = quarter_dict[4]
			if MM == "01":
				QQ = quarter_dict[4]

				###
				#	This means it is a January of 201N, but filing is really about the last quarter of 201(N-1).  Do the needful!
				###
				YYYY = str(int(YYYY)-1)
				
			try:	
				#print "5 classifying label "+label+" with value "+value+" as "+YYYY+QQ+" with MM "+MM+" with ABCD = "+ABCD+" and format "+format
				period[label] = YYYY+QQ
			except:
				print "Couldn't assign: "+str(label)
				print "MM: "+str(MM)
				print "value: "+str(value)
				period[label] = "INVALID FORMAT"


		#print "period = "+period[label]
		#print "year = "+ YYYY
		#print "quarter = "+ QQ

	#so, now i have a dict (period) that looks like this:
	#{label1: "20110331", label2: "20110630", label3: "20110630" }
	#and i also have a context_counts dict that got passed to me, that looks like
	#{label1: 4, label2: 8, label3: 2 }


	# Now, remove all quarters where the quarter is not the previous quarter or the quarter before the previous quarter. 
	# THIS WILL HAVE TO BE CHANGED TO SUPPORT A COMPANY "FIXING"  A VALUE FROM A PREVIOUS FILING
	# But supporting that is R2!

	# Use date_id_dict to do this.  Create a list of all the values in period, then sort it descending, then walk through it (in order)
	# keeping track of the previous value.  if file_date_id is between date_dict_id[value] and date_dict_id[previous_value], then that period, 
	# and the two following are allowed, everything else is canned.

	set_flag = 0
	set_count = 0	
	permitted_values = []
	previous_date_id = 0
	dupped_period_list = []
	period_list = []

	#print "period = "+str(period)


	#DEBUG
	# PRINT THE ENTIRE PERIOD DICT
	#for label in period:
	#	print label, period[label]
		
	for p_label in period:
		dupped_period_list.append(period[p_label])

	period_list = list(set(dupped_period_list))	
	sorted_date_id_values = sorted(date_id_dict.values(), reverse=True)

        for date_id in sorted_date_id_values:
                if previous_date_id == 0:
                        previous_date_id = date_id
                        continue

                if set_flag == 1:
			set_count = set_count + 1
                        for d in date_id_dict:
#                               if date_id == date_id_dict[d]:
                                if previous_date_id == date_id_dict[d]:
                                        permitted_values.append(d)
                                        break
                        
                if file_date_id < previous_date_id and file_date_id >= date_id:
                        set_flag = 1
			for d in date_id_dict:
#                               if date_id == date_id_dict[d]:
                                if previous_date_id == date_id_dict[d]:
                                        permitted_values.append(d)
                                        break
                if set_count == 3:
                        break

                previous_date_id = date_id


	#print "permitted_values = "+str(permitted_values)	


	#so, now, i create a new dict that is a unique list of values in the period dict as the key, and the count of all instances of that period, 
	#it will look like
	#{"20110331": 4, "20110630":2, "20110930":1}

	#print period

	# Initialize
	period_count = {}
	period_permitted_count = {}
	for label in context_counts:
		try:
			period_permitted_count[period[label]] = 0
			period_count[period[label]] = 0
		except:
			pass

	# Populate
	for label in context_counts:
		try:
			period_count[period[label]] = period_count[period[label]] + context_counts[label]
			# ONLY HAS A GREATER THAN 0 COUNT IF ITS A PERMITTED VALUE!!
			if period[label] in permitted_values:   
				period_permitted_count[period[label]] = period_permitted_count[period[label]] + context_counts[label]

		except:
			print "couldn't work for: "+ label
	

	#for i in period_count:
	#	print i, period_count[i]


	"""	
	then, i take the one with the highest count. If it is not more than 10 then this fails.  If it is above ten, it returns that period
	"""

	#print "peroid = "+str(period)
	#print "period_count = "+ str(period_count)
	#print "candidate_count = "+ str(candidate_count)

	"""
	print "Pre cleanse:"
	for i in period_count:
		print i, period_count[i]
	print "Post cleanse:"
	for i in period_permitted_count:
		print i, period_permitted_count[i]
	"""


	#print "printing period pre"
	#for i in period:
	#	print "printing period"
	#	print "period = "+i+", "+period[i]
	try:
		candidate_count = sorted(period_permitted_count.values(), reverse=True)[0]
	except:
		print "Bail!"
		sys.exit(1)	

	permitted_list = []	
	for i in period_permitted_count:
		#print "ppc "+i, period_permitted_count[i]
		if period_permitted_count[i] == candidate_count:
			permitted_list.append(i) # I have to do this because multiple quarters could have had the same count




	candidate = sorted(permitted_list,reverse=True)[0]

	# Now, one last pass. Go back through and update any row with the accepted enddate as the right quarter
	# take a sample, find one with a ";" with the right quarter, get the end date
	# now, i cycle through everything
	# if it has a ";" then check the end date, if it is the same as the sample, then add set the quarter

	"""
	print "Old Period"
	#for i in period:
	#	print str(i), context_values[i], period[i]

	for i in period:
		if candidate == period[i] and context_values[i].find('|;|') != -1:
			sampled_end_date = context_values[i][context_values[i].index('|;|')+3:]
			break

	print "Sample date = "+sampled_end_date

	new_period = {}
	for i in period:
		new_period[i] = period[i]

	for i in period:
		if context_values[i].find('|;|') != -1:
			if context_values[i][context_values[i].index('|;|')+3:] == sampled_end_date:
				print "exchanging for context_value = "+context_values[i]
				new_period[i] = candidate	
	print "New Period"
	#for i in period:
	#	print "new "+str(i), context_values[i], period[i] 
	"""
		





	#print "sorted period count ", str(sorted(period_count.keys(), reverse=True)[0])
	#print "period_count "+ str(period_count)
	#print "winning candidate "+ str(candidate)
	#print "period "+str(period)



	



	if candidate_count > 9:
		#period = candidate	
		return [candidate, period, period_quarter_map[candidate]]
	else:
		print "Could NOT determine the period for this file!"
		print "file_date_id = "+str(file_date_id)
		for i in  period_permitted_count:
			print i, period_permitted_count[i]
		return ["FAIL", "FAIL","FAIL"]
		

		
