#!/usr/bin/python

#
# Usage:
#  extract_quarter.py  2005 3 


import sys
import os
import os.path
import xbrl_load_quarter
import shutil
from subprocess import call
from datetime import datetime


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

iy = year
if quarter == "1":
	iq = "2"
if quarter == "2":
	iq = "3"
if quarter == "3":
	iq = "4"
if quarter == "4":
	iq = "1"
	if year == "2011":
		iy = "2012"


#sec_index_fn = "ftp://ftp.sec.gov/edgar/full-index/"+year+"/QTR"+quarter+"/master.idx"
#local_index_fn = index_path+"/"+year+"."+quarter
sec_index_fn = "ftp://ftp.sec.gov/edgar/full-index/"+iy+"/QTR"+iq+"/master.idx"
local_index_fn = index_path+"/"+iy+"."+iq


if  os.path.isfile(local_index_fn) == False:
	print "Extracting "+local_index_fn
	call(["wget","-q" ,"-O",local_index_fn ,sec_index_fn])

f  = open(local_index_fn)


i = 0
count = 0
for record in f:
	i = i + 1
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
	local_fn = path+"/"+name+"_10q_"+year+"q"+quarter+".dat" 
	loaded_fn = loaded_path+"/"+name+"_10q_"+year+"q"+quarter+".dat"
	not_xbrl_fn = not_xbrl_path+"/"+name+"_10q_"+year+"q"+quarter+".dat"
	error_fn = error_path+"/"+name+"_10q_"+year+"q"+quarter+".dat"
	error_canada_fn = error_canada_path+"/"+name+"_10q_"+year+"q"+quarter+".dat"


	if  form == "10-Q":
		#print "extracting file to: "+local_fn
		if os.path.isfile(loaded_fn):
			continue
			shutil.move(loaded_fn,local_fn)
		if os.path.isfile(not_xbrl_fn):
			continue
			shutil.move(not_xbrl_fn,local_fn)
		if os.path.isfile(error_fn):
			continue
			shutil.move(error_fn,local_fn)
		if os.path.isfile(error_canada_fn):
			continue
			shutil.move(error_canada_fn,local_fn)

		if os.path.isfile(local_fn) == False:
			#print "wget -O "+local_fn+" ftp://ftp.sec.gov/"+sec_fn 
			print "Extracting "+local_fn
			call(["wget","-q", "-O", local_fn, "ftp://ftp.sec.gov/"+sec_fn])
		else:
			print "Already extracted "+local_fn
		
		#period = get_period(local_fn)
		if is_xbrl(local_fn) == 0:
			#shutil.move(local_fn,loaded_path+"/"+local_fn[local_fn.rindex("/")+1:].replace(".","__"+str(datetime.now()).replace(" ","_")+"."))
			print "Not an xbrl file, moving to: "+not_xbrl_fn
			shutil.move(local_fn,not_xbrl_fn)

#		elif period == 0:
#			print "No period!"
#		elif supported_periods.__contains__(period):	
#			print "Loading period: "+period
#			result = xbrl_load_quarter.xbrl_load(local_fn, name, cik, period, file_date, valid_dates)		
		else:

			result = xbrl_load_quarter.xbrl_load(local_fn, name, cik, file_date)		
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
			count = count + 1
			#if count == 5:
			#	break
f.close()
