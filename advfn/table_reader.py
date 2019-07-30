#!/usr/bin/python

import pprint 
import re
import sys
import urllib
from table_parser import *

debug = 0

def lprint(text):
	if debug == 1:
		print text

def find_year(field):
	years = ["2008","2009","2010","2011","2012","2013","2014"]
	for year in years:
		if field.find(year) != -1:
			return([True,year])
	return([False,0])

def fix_second_year(db):
	#print str(db)
	if db[0][0][2] < db[0][1][2]:
		db[0][1][1] = str(int(db[0][0][1]) -1)
	if db[0][1][2] == -99:
		db[0][1][1] = str(int(db[0][0][1]) -1)
		db[0][1][2] = str(int(db[0][0][2]))
		
	return(db)


"""
#org
def fix_second_year(db):
	print str(db)
	if db[0][2] > db[1][2]:
		db[1][1] = str(int(db[0][1]) -1)
	if db[1][2] == -99:
		db[1][1] = str(int(db[0][1]) -1)
		db[1][2] = str(int(db[0][2]))
		
	return(db)

"""
		
def find_month(field):
	text_months = ["january","february","march","april","may","june","july","august","september","october","november","december"]
	month_map = {}
	for i,value in enumerate(text_months):
		month_map[value] = str(i+1).zfill(2)

	range_3_map = {}
	for i in range(12):
		if i+1 > 3:
			range_3_map[str(i+1).zfill(2)] = str(i+1-3).zfill(2)
		else:
			range_3_map[str(i+1).zfill(2)] = str(i+1+9).zfill(2)
		
			
	range_6_map = {}
	for i in range(12):
		if i+1 > 6:
			range_6_map[str(i+1).zfill(2)] = str(i+1-6).zfill(2)
		else:
			range_6_map[str(i+1).zfill(2)] = str(i+1+6).zfill(2)

	range_9_map = {}
	for i in range(12):
		if i+1 > 9:
			range_9_map[str(i+1).zfill(2)] = str(i+1-9).zfill(2)
		else:
			range_9_map[str(i+1).zfill(2)] = str(i+3+1).zfill(2)



	for mth in text_months:
	#		if field.lower().find(mth) != -1:
		if field.lower().find(mth) != -1 and field.lower().find("ended") != -1:
			if field.lower().find("three") != -1:
				return([True, month_map[mth], range_3_map[month_map[mth]]])
			elif field.lower().find("six") != -1:
				return([True, month_map[mth], range_6_map[month_map[mth]]])
			elif field.lower().find("nine") != -1:
				return([True, month_map[mth], range_9_map[month_map[mth]]])
			elif field.lower().find("twelve") != -1:
				return([True, month_map[mth], -99]) # Use -99, because you want to show the same month, but i need to communicate to the parent function that the year should decrement
			elif field.lower().find("year") != -1:
				#print "PMB found month! "+field
				return([True, month_map[mth], -99]) # Use -99, because you want to show the same month, but i need to communicate to the parent function that the year should decrement
		if re.match(mth,field.lower().replace(" ","")) != None: # I only care if you are the first word
			return([True, month_map[mth], -1])
			
		
	return[False,0,-1]

def combine_ended_to_date(table):
	# Goal, when you have "X months ended" on one row, and dates on the next, combine them together 
	# [Three Months Ended,Six Months Ended]
	# [November24,2012, November26,2011, November24,2012, November26,2011]
	# becomes
	# [Three Months Ended November24,2012, Three Months Ended November26,2011,Six Months Ended November24,2012, Six Months Ended November26,2011]

	text_months = ["january","february","march","april","may","june","july","august","september","october","november","december"]
	month_map = {}
	temp_table = []


	for i,value in enumerate(text_months):
		month_map[value] = str(i+1).zfill(2)


	buffer = []

	for row in table:
		new_row = []
		if row[0].lower().find("ended") != -1 and not find_month(row[0])[0]:
			#print "found "+str(row) +"|"+str(find_month(row[0]))
			buffer = row
			continue
			
		if buffer != []:
			#print "and the next line is "+str(row)+" for buffer "+str(buffer)
			for mth in text_months:
				if row[0].lower().find(mth) != -1:
					# the following row has a month!
					num_fields = len(row)
					ended_fields = len(buffer)
					if num_fields == 4 and ended_fields == 2:
						new_row.append(buffer[0] +" "+row[0])
						new_row.append(buffer[0] +" "+row[1])
						new_row.append(buffer[1] +" "+row[2])
						new_row.append(buffer[1] +" "+row[3])
 
					if num_fields == 2 and ended_fields == 2:
						new_row.append(buffer[0] +" "+row[0])
						new_row.append(buffer[1] +" "+row[1])

				# or, for opposite day
				"""
				elif buffer[0].lower().find(mth) != -1:
					num_fields = len(row)
					ended_fields = len(buffer)
					if num_fields == 2 and ended_fields == 1:
						#print "here for "+row[0]
						new_row.append(buffer[0] +" "+row[0])
						new_row.append(buffer[0] +" "+row[1])
				"""
					  

	
			buffer = []

		if new_row == []:
			new_row = row
		
		temp_table.append(new_row)	
			
	return(temp_table)			

	



def remove_dupes(table):
	"""
	First pass, 
	No dupes in row[0] and [2], if a dupe, all get dropped, no winner
	Second pass,
	if any of those dupes identicle for row[0] [1] [2], then append one of them
	"""

	dupe_table = []
	temp_table = []
	dupe_store = []

	for entry in table:
		if temp_table.__contains__([entry[0],entry[2]]):
			dupe_table.append([entry[0],entry[2]])
			dupe_store.append(entry)
		else:
			temp_table.append([entry[0],entry[2]])
	temp_table = []
	for entry in table:
			if not dupe_table.__contains__([entry[0],entry[2]]):
				temp_table.append(entry)


	#print "dupes"
	#for entry in dupe_store:
	#	print str(entry)
	#print "end dupes"
	
	# Second pass
	dupe_temp_table =  dupe_store

	for entry in dupe_store:
		cnt =  dupe_temp_table.count(entry)
		if cnt >= 1:
			temp_table.append(entry)
			for index in range(cnt):			
				dupe_temp_table.remove(entry)
		
			


			
		
		
			
	#for i in dupe_table:
	#	print "dupe "+str(i)

	return(temp_table)


def am_i_a_date(field):
	return(find_month(field)[0])
		

def fix_sign(table):
	temp_table = []
	for entry in table:
		temp_entry = entry
		try:
			if entry[1].find("(") != -1:
				temp_entry[1] = temp_entry[1].replace("(","-")
		except:
			pass
		temp_table.append(temp_entry)
	return(temp_table)


def fix_magnitude(table,magnitude):
	temp_table = []
	for entry in table:
		temp_entry = entry
		try:
			if magnitude[0] == "th":
				#print temp_entry[1]
				temp_entry[1] = temp_entry[1].replace(",","") + "000"
				#print temp_entry[1]
		except:
			pass
		temp_table.append(temp_entry)
	return(temp_table)


def remove_bad_rows(table):
	"""
        2) row[0] must have len > 3, if else drop
        3) row[1] may only contain [0-9],",",".","(",")", if else drop <- COULD BE A DATE!
        4) if find  "(" in row[1], replace with "-" and remove ")" if present
	"""
	temp_table = []
	for entry in table:
		if len(str(entry[0]))  > 3:
			temp_table.append(entry)

	table = temp_table
	#for row in table:
	#	print row

	temp_table = []
	for entry in table:
		# Remove everything that I think *could* be in buffer, if it is empty, then i can continue
		try:
			buffer = entry[1]
			buffer = re.sub("[0-9]","",buffer)	
			buffer = buffer.replace(".","").replace(",","").replace("(","").replace(")","").replace("$","").replace(" ","")
			#print "buffer1 = |"+buffer+"|",str(re.sub("[0-9]","",buffer)),"end",entry[1]
			if am_i_a_date(entry[0]) or len(buffer) == 0:
				if len(buffer) == 0:
					for i,value in enumerate(entry):
						if i == 0:
							continue
						entry[i] = entry[i].replace("(","-").replace(")","").replace("$","").replace(" ","")

				temp_table.append(entry)
		except:
				temp_table.append(entry)

	#for row in temp_table:
	#	print "after"+str(row)
	return(temp_table)


def clean_dates(table):		
#5) keep a date buffer, if find a year "2012" and a full text month is found, this date 
#ill apply  to the column + 1 until another instance is found in a new row
#        6) if one row has full text month followed by next row with years, apply years to previ
#us row  ( cleaning )
#        7) Look for "Three Months" "Six Months" "Nine Months" "12 Months" "1 Year" before, in, 
#r after a full text month, and  make the date value |:|
#        8) if a full text month is in row[]0 and, row[1] has numbers and comma's only, ignore e
#erything until you get to a row with a valid date
#        9) if no year in a row with valid dates, and year isn't in row[0] of next row, drop and
#contineu until a valid date is found
#        10) replace "\n" with ""
#        11) if rows do not have tag + values (enough values listed ) for the dates listed. i.e.
#
	# remove the weird dates, kill everything till the next valid date
	
	# combine the dates that are next to eachother in one entry
	#temp_table = table
	temp_table = []
	pull_year = 0
	proceed_due_to_bad_date = 0

	# Find a row with a text month and a year defined
	date_buffer = []
	pre_table_buffer = []

	for entry in table:
		#print "line = "+str(entry),
		#print "pdtbd = "+str(proceed_due_to_bad_date),
		#print " pull year = "+str(pull_year)


		if entry[0].find("href")  != -1 or entry[0].lower().find("consolidated") != -1 or entry[0].lower().find("statement") != -1:
			proceed_due_to_bad_date = 1
			continue
		if pull_year == 1:
			year_list = []
			found_year = 0
			for field in entry:
				year_result = find_year(field)
				if year_result[0]:
					found_year = 1
					year_list.append(year_result[1])

			if len(date_buffer) == 2 and len(year_list)  == 4:
				# Duplicate each entry in date_buffer
				year_list.pop()
				year_list.pop()

				new_date_buffer = []
				for db in date_buffer:
					new_db = []
					new_db.append([db[0][0], year_list[0], db[0][2],db[0][3]])
					new_db.append([db[1][0], year_list[0], db[1][2],db[1][3]])
					new_date_buffer.append(new_db)
					new_db = []
		
					new_db.append([db[0][0], year_list[1], db[0][2],db[0][3]])
					new_db.append([db[1][0], year_list[1], db[1][2],db[1][3]])
					new_date_buffer.append(new_db)



				date_buffer = new_date_buffer

			elif len(date_buffer) == 2 and len(year_list) == 2:
				for i,year in enumerate(year_list):
					date_buffer[i][0] = [date_buffer[i][0][0],str(year),date_buffer[i][0][2],date_buffer[i][0][3]]
					if len(date_buffer[i][1]) != 0:
						date_buffer[i][1] = [date_buffer[i][1][0],str(year),date_buffer[i][1][2],date_buffer[i][1][3]]

				for i,year in enumerate(year_list):
					if len(date_buffer[i][1]) != 0:
						new_date_buffer = []
						for db in date_buffer:
							new_db = fix_second_year(db)
							new_date_buffer.append(new_db)
						date_buffer = new_date_buffer
				
			elif len(date_buffer) == 1 and len(year_list) == 2:
				print "yoyo "+str(date_buffer)+", "+str(len(year_list))
				
			#elif len(date_buffer) == 1 and len(year_list) == 1:
			else:
				lprint("some wierd combination of months/years")
				lprint("date buffer = "+str(date_buffer))
				lprint("year_list = "+str(year_list))

			if found_year == 0:
				proceed_due_to_bad_date = 1
				continue
			pull_year = 0
			#print "Done processing this row!"
			continue
					
		#print "PMB entry0 = "+str(entry)

		# Supports: 
#['Three Months Ended December 31,', 'Nine Months Ended December 31,']
#['2012', '2011', '2012', '2011']

		# Trying ['Year Ended December 31, 2011', 
#['Year Ended December 31,']
#['2011', '2010']



		if find_month(entry[0])[0]:
			proceed_due_to_bad_date = 0
			date_buffer = []
			found_year = 0
			#print "found a month in the first cell: "+entry[0] 
			for field in entry:
				if re.sub("\D","",field).replace(",","") == "": # an field after a defined date is only numbers, i can't deal with this
					proceed_due_to_bad_date = 1
					continue
				mth_result = find_month(field)
				if mth_result[0]:
					print "found a month in another cell: "+field
					year_result = find_year(field)
					#print "did i find a year?  = "+str(year_result)
					if year_result[0]:
						found_year = 1
						# "September30,2012
						day = re.sub("\D","",field.replace(year_result[1],""))
						if mth_result[2] == -1:
							date_buffer.append([[field,str(year_result[1]),str(mth_result[1]),day],[]])
						if mth_result[2] != -1:
							date_buffer.append([[field,str(year_result[1]),str(mth_result[1]),day],[field,str(year_result[1]),str(mth_result[2]),day]]) 
							date_buffer = fix_second_year(date_buffer)
					else:
						#Sept30, Sept30
						day = re.sub("\D","",field)
						if mth_result[2] == -1:
							date_buffer.append([[field,None,str(mth_result[1]),day],[]])
						if mth_result[2] != -1:
							date_buffer.append([[field,None,str(mth_result[1]),day],[field, None,str(mth_result[2]),day]]) 
						print "hiya found a month in another cell: "+str(date_buffer), str(len(date_buffer))



			if found_year == 0:
				# "September30
				# 2012
				# Must go to next row, but first pull *all* the dates on this row
				pull_year = 1

			#print "Done processing this row!"
			continue
						
						
		if proceed_due_to_bad_date == 1:
			continue								


	
				
		# Theoretically i now have a date	
		num_dates = len(date_buffer)

		#print str(entry), str(num_dates)

		if num_dates == 0:
			continue

		# I expect to get as many values as i get dates
		value_list = []			
		for i, value in enumerate(entry):
			if i == 0:
				attribute = value
			else:
				value_list.append(value)

		if len(value_list) != num_dates:
			lprint("I have "+str(num_dates)+" dates and "+str(len(value_list))+" values. What do i do?!")
			lprint("dates = "+str(date_buffer))
			lprint("values = "+str(value_list))
			lprint( "field = "+str(entry))
			proceed_due_to_bad_date = 1
			continue

		##if attribute == " State":
		#	print "test"
		#	print value_list	
		#	for value in value_list

		bad_value = 0
		for value in value_list:
			if find_year(value)[0]:
				lprint("found year in value "+value)
				bad_value = 1
				break
		if bad_value == 1:
			continue


		for i,value in enumerate(value_list):
			#print "appending: "+attribute,value, str(date_buffer)
			try:
				if len(date_buffer[i][1]) == 0:
					temp_table.append([attribute, value, str(date_buffer[i][0][1]+"-"+date_buffer[i][0][2]+"-"+date_buffer[i][0][3])])
				else:
					temp_table.append([attribute, value, str(date_buffer[i][1][1]+"-"+date_buffer[i][1][2]+"-"+date_buffer[i][1][3]+"|;|"+date_buffer[i][0][1]+"-"+date_buffer[i][0][2]+"-"+date_buffer[i][0][3])])
			except:
				pass
			"""
			# Reversed
			else:
				temp_table.append([attribute, value, str(date_buffer[i][0][1]+"-"+date_buffer[i][0][2]+"-"+date_buffer[i][0][3]+"|;|"+date_buffer[i][1][1]+"-"+date_buffer[i][1][2]+"-"+date_buffer[i][1][3])])
			"""

		
	return(temp_table)
 
			
				



		


	# determine month:
		# look for a match with the text_month list

	# determine year:
		#look for a match with the "year" list			

	# determine day:
		# remove the year by cycling through the year list, replacing with ""
		# find the day with: re.sub("\D","",field)

		

def main(fn):

	#f = urllib.urlopen('http://myweb.com/data.html')
	#f = urllib.urlopen('http://www.sec.gov/Archives/edgar/data/1000045/000119312512462945/d402577d10q.htm')
	f = open(fn)
	p = TableParser()
	p.feed(f.read())
	f.close()
	table = []
	magnitude = []
	#pprint.pprint(p.doc)
	#sys.exit(0)
	for i in p.doc:
		for j in i:
			#print i	
			line = ""
			row = []
			for z in j:
				try:
					if str(z) != "[]":
						line = line+" "+ str(z[0])
						#print "|"+str(z[0])+"|",
						if re.search("[0-9]",str(z[0])) != None or re.search("[a-z]",str(z[0]).lower()) != None or z[0].lower().find("ended") != -1:
							#print "|inside|"+str(z[0])+"|",
							row.append(z[0])
							if z[0].lower().find("in thousand") != -1:
								magnitude.append("th")
							"""
							if z[0].find("141") != -1:
								print str(line)
							if z[0].find("equivalents") != -1:
								print str(line)
							"""
				except:
					pass
			#print line				
			#print
			try :
				#re.search("[0-9]",line).group(0)	
				#line.find(",")
				re.search("[0-9]",row[1]).group(0)	
				row[1].find(",")
				#row[1] = row[1].replace(",","")
				table.append(row)
			except:
				try:
					if row[0].lower().find("ended") != -1:
						table.append(row)
				except:
					pass

	#print "Start"
	#for row in table:
	#	print row 
	#print "mid"

	temp_table = []
	for row in table:
		temp_row = []
		for entry in row:
			temp_row.append(str(entry).replace("\n",""))
		temp_table.append(temp_row)	

	table = temp_table

	#print "pre"
	#for row in table:
	#	print row 
	table = combine_ended_to_date(table)

	#print "post"
	#for row in table:
	#	print row 


	table = remove_bad_rows(table)
	#print "stuff"	
	#for row in table:
	#	print row 
	#print "after"	


	for row in table:
		print row
	table = clean_dates(table)

	table = remove_dupes(table)
	for row in table:
		print row
	#print magnitude
	table = fix_magnitude(table,magnitude)
	table = fix_sign(table)
	#print "OUTPUT"

	return table

		
		
if __name__ == '__main__':
	fn = sys.argv[1]
	data = main(fn)
	for row in data:
		print row
	
		



 
