#!/usr/bin/python

#
# Usage:
#  extract_quarter.py  2005 3 


import sys
import os
import os.path
import xbrl_load_quarter
import shutil
import MySQLdb
from subprocess import call
from datetime import datetime


def determine_symbol(file):
	"""
	I walk through the whole file, and look for this pattern:
	"<[a-z]:"
	The pattern that occurs the most often, that is not one that I'm expecting, like "us-gaap", i interpret as the symbol
	"""


	tag = []
	tag_count = {}
	found_tag = ""
	for line in f:
		try:
			if line.find("<") != -1 and line.find(":") != -1:
				if line.index("<") < line.index(":"):
					found_tag = line[line.index("<")+1:line.index(":")]
					if found_tag.find(" ") != -1:
						found_tag = ""
						continue
			try:
				tag_count[found_tag] =  tag_count[found_tag]  + 1
			except:
				tag_count[found_tag] = 0
			found_tag = ""
		except:
			found_tag = ""
			pass

	del tag_count[""]
	del tag_count["link"]
	del tag_count["us-gaap"]
	for key_list in tag_count.keys():
		if key_list.find("xbrl") != -1:
			del tag_count[key_list]

	for i in tag_count:
		tag.append([i,tag_count[i]])
	tag.sort(key=lambda r: r[1], reverse=True)
	return(tag[0][0])



def is_xbrl(file):
	f = open(file)
	xbrl = 0
	for record in f:
		if record.find("<us-gaap:") != -1:
			xbrl = 1
			break
	return xbrl
	

def get_period(file):
	f = open(file)
	period = 0
	for record in f:
		if record.find("CONFORMED PERIOD OF REPORT") != -1:
			period = record.split("\t")[1]
			break
	return period


conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()



year = sys.argv[1]
quarter = sys.argv[2]

#valid_dates =  __import__("xbrl_"+year+"q"+quarter+"_valid_dates")
#supported_periods = ["20110331","20110630","20110930","20111231","20120331","20120630","20120930","20121231"]


index_path = "/media/data/investments/data/edgar/indexes"
path = "/media/data/investments/data/edgar/forms/"+year+"q"+quarter
loaded_path = "/media/data/investments/data/edgar/forms/"+year+"q"+quarter+"/loaded"
not_xbrl_path = "/media/data/investments/data/edgar/forms/"+year+"q"+quarter+"/not_xbrl"
error_path = "/media/data/investments/data/edgar/forms/"+year+"q"+quarter+"/error"
error_canada_path = "/media/data/investments/data/edgar/forms/"+year+"q"+quarter+"/error/canada"



file_date = str(datetime.now()).split(" ")[0]

call(["mkdir","-p", index_path])
call(["mkdir","-p", path])
call(["mkdir","-p", loaded_path])
call(["mkdir","-p", not_xbrl_path])
call(["mkdir","-p", error_path])
call(["mkdir","-p", error_canada_path])


sec_index_fn = "ftp://ftp.sec.gov/edgar/full-index/"+year+"/QTR"+quarter+"/master.idx"
local_index_fn = index_path+"/"+year+"."+quarter


#sec_index_fn = "ftp://ftp.sec.gov/edgar/full-index/"+iy+"/QTR"+iq+"/master.idx"
#local_index_fn = index_path+"/"+iy+"."+iq


if  os.path.isfile(local_index_fn) == False:
	print "Extracting "+local_index_fn
	call(["wget","-q" ,"-O",local_index_fn ,sec_index_fn])

local_f  = open(local_index_fn)


i = 0
count = 0
for record in local_f:
	count = count + 1

print "len f = "+str(count)
local_f.close()
local_f  = open(local_index_fn)
count = 0

for record in local_f:
	#print "count = "+str(count)
	if count == 1:
		break
	count = count + 1
	try:
		with open('run_history_extract') as t: pass
	except IOError as e:
		print '"run_history_extract" file has been removed, gracefully exiting'
		break

	parsed = record.split("|")
	try:
		 int(parsed[0])
	except:
		 continue

	# CIK|Company Name|Form Type|Date Filed|Filename
	cik = parsed[0]
	name = parsed[1].replace(" ","_").replace("/","")
	form = parsed[2]
	file_date = parsed[3]

	sec_fn = parsed[4].replace("\n","")
	local_fn = path+"/"+name+"_10q_"+year+"q"+quarter+".xbrl" 
	loaded_fn = loaded_path+"/"+name+"_10q_"+year+"q"+quarter+".xbrl"
	not_xbrl_fn = not_xbrl_path+"/"+name+"_10q_"+year+"q"+quarter+".dat"
	error_fn = error_path+"/"+name+"_10q_"+year+"q"+quarter+".err"
	error_canada_fn = error_canada_path+"/"+name+"_10q_"+year+"q"+quarter+".dat"


	if  form == "10-Q" or form == "10-K" or form == "8-K":
		#print "extracting file to: "+local_fn
		if os.path.isfile(loaded_fn):
			continue
			#shutil.move(loaded_fn,local_fn)
		if os.path.isfile(not_xbrl_fn):
			continue
			#shutil.move(not_xbrl_fn,local_fn)
		if os.path.isfile(error_fn):
			continue
			#shutil.move(error_fn,local_fn)
		if os.path.isfile(error_canada_fn):
			continue
			#shutil.move(error_canada_fn,local_fn)

		if os.path.isfile(local_fn) == False:
			#print "wget -O "+local_fn+" ftp://ftp.sec.gov/"+sec_fn 
			print "Extracting "+local_fn
			print "CIK = "+str(cik)	
			call(["wget","-q", "-O", local_fn, "ftp://ftp.sec.gov/"+sec_fn])
		else:
			print "Already extracted "+local_fn
		
		if is_xbrl(local_fn) == 0:
			#shutil.move(local_fn,loaded_path+"/"+local_fn[local_fn.rindex("/")+1:].replace(".","__"+str(datetime.now()).replace(" ","_")+"."))
			print "Not an xbrl file, moving to: "+not_xbrl_fn
			shutil.move(local_fn,not_xbrl_fn)

		else:

			# find date_id from file_date
		        cursor.execute(" select date_id from dates where date = \""+str(file_date)+"\"")
			date_id = str(cursor.fetchone()[0])
			try:

				cursor.execute(" select company_sk from company where cik = \""+str(cik)+"\"")
				company_sk = str(cursor.fetchone()[0])
				cursor.execute("delete from gaap_value where file_date_id = "+date_id+" and company_sk = "+company_sk)
				conn.commit()
			except:
				pass



			# figure out how to find the symbol from that date/name
			cursor.execute(" select symbol from symbol where cik = \""+str(cik)+"\" and start_date_id < "+date_id+" and end_date_id < "+date_id)
			try:
				symbol = cursor.fetchone()[0]
			except:
				try:
					symbol = determine_symbol(local_fn)
				except:
					symbol = "DNE"

			result = xbrl_load_quarter.xbrl_load(local_fn, name, cik, file_date, form, symbol)

			if result == 0:
				#shutil.move(local_fn,loaded_path+"/"+local_fn[local_fn.rindex("/")+1:].replace(".","__"+str(datetime.now()).replace(" ","_")+"."))
				print "Success!  Moving to: "+loaded_fn
				shutil.move(local_fn,loaded_fn)
			elif result == 1:
				#shutil.move(local_fn,error_path+"/"+local_fn[local_fn.rindex("/")+1:].replace(".","__"+str(datetime.now()).replace(" ","_")+"."))	
				print "Error! Moving to: "+error_fn
				shutil.move(local_fn,error_fn)
			elif result == 2:
				#shutil.move(local_fn,error_canada_path+"/"+local_fn[local_fn.rindex("/")+1:].replace(".","__"+str(datetime.now()).replace(" ","_")+"."))
				print "This company is in Canada! Get off your ass and support me!  Moving to: "+error_canada_fn
				shutil.move(local_fn,error_canada_fn)
			#if count == 5:
			#	break
local_f.close()

cursor.close()
conn.close()

