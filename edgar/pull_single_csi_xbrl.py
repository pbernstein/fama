#!/usr/bin/python

#
# Usage:

import re
import sys
import time
from datetime import datetime
import os
import os.path
import glob
from subprocess import call
from subprocess import check_output
import feedparser
import hashlib
import MySQLdb
import shutil
import utility
import xbrl_load_quarter
import html_load_gaap
import cleanse
import send_generic_email_attachment as send_email
from eod import fulfill_id as fulfill_id
from eod import fulfill_raw as fulfill_raw
from eod import fulfill_html as fulfill_html
import table_reader as table_reader
import tweet
import clean_txt_html
import clean_txt_xbrl
import erase_filing
import tarfile


conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()





path = "/media/data/investments/data/edgar/forms/rss/"
temp_path = "/media/data/investments/data/edgar/forms/eod/forms/csi"
loaded_path = "/media/data/investments/data/edgar/forms/rss/loaded/"
error_path = "/media/data/investments/data/edgar/forms/rss/error/"


#date = str(unicode(datetime.today())[:10]).replace("-","")

file_date = sys.argv[1]
date = file_date.replace("-","")
year = date[:4]
if year < '2014':
	bkp_path = "/media/data/investments/data/edgar/forms/eod/form_bkp/"+year+"/"
else:
	bkp_path = "/media/data/investments/data/edgar/forms/eod/form_bkp/"

cursor.execute(" select date_id from dates where date = \""+str(date)+"\"")
row = cursor.fetchone()
date_id = row[0]

print "Removing all filings for "+date
cursor.execute(" delete from extract_history where date_id = "+str(date_id))
cursor.execute(" delete from gaap_value where file_date_id = "+str(date_id))
cursor.execute(" delete from ins_value where date_id = "+str(date_id))
conn.commit()




#url = 'ftp://ftp.sec.gov/edgar/daily-index/2013/QTR1/master.'+date+'.idx.gz'

call(["rm", "-rf", temp_path])
call(["mkdir", "-p", temp_path])

if os.path.exists(bkp_path+"eod_"+date+".tar.gz") and os.stat(bkp_path+"eod_"+date+".tar.gz").st_size != 142:
	print "Expanding found file at: "+bkp_path+"eod_"+date+".tar.gz"
	os.system("tar -xzf "+bkp_path+"/eod_"+date+".tar.gz -C "+temp_path+" --strip 8")
	print "tar -xzf "+bkp_path+"/eod_"+date+".tar.gz -C "+temp_path+" --strip 8"


idx_name = "/media/data/id/hpcc/chTicker_csi_all_pipes_with_8k"
idx_handle = open(idx_name)


for idx_record in idx_handle:
	if re.search("[0-9]",idx_record[0]) != None:

		idx = idx_record.split("|")
                cik = idx[2]
                cik = cik.zfill(10)
                name = idx[1]
                form = idx[3]
                exchange = idx[8].replace("\n","")
                symbol = idx[7]
		if symbol.upper() != "LUB":
			continue

                filing_date_id = idx[4]
                if str(filing_date_id) == str(date_id) and (form ==  '10-Q' or form == '10-K' or form == '8-K'):
			txt_url = "ftp://ftp.sec.gov/"+idx[5].replace("\n",'')
	
			fn_name = utility.clean_name(name)
			basename = fn_name.replace(" ","_").replace('/',"")+"_"+form.replace(" ","_").replace('/',"")

			# so matching against an int kicks out a warning


			txt_name = temp_path+basename+"_eod.txt"
			print "txt_name "+txt_name
			must_repull = 0 

			new_file = 1

			if symbol == "NA":
				continue
			else:
				print "Extracting "+symbol, form
				#print "new file: "+fn_name, form, period	
				if not os.path.exists(txt_name) or os.stat(txt_name).st_size == 0:
						####
						# BIG NOTE!   THIS IS NOT FOR THE DAILY!
						# THIS IS BECUASE I PULLED THE DATA FROM THE FTP SITE
						# AND I DID NOT EXTRACT FILINGS WITH NO SYMBOL!

						print "WGET A FILE! for "+txt_name
						#sys.exit(0)
						#continue
						call(["wget", "-qN", "-O", txt_name, txt_url])

		
				# FIND PERIOD, THIS IS HERE BECAUSE ITS A FRESH PULL
				period = date
				filing_ts = ""
				txt_handle = open(txt_name)
				for txt_record in txt_handle:
					if txt_record.find("CONFORMED PERIOD OF REPORT") != -1:
						period = txt_record.split(":")[1].strip()
						print " found period "+period
					if txt_record.find("<ACCEPTANCE-DATETIME>") != -1:
						filing_ts = txt_record.split(">")[1].strip()
						print " found filing_ts "+filing_ts
				
				if filing_ts == "":
					print "no filing_ts, continuing"
					continue
				### XBRL ###
				t0 = time.time()

				txt_xbrl_holder = []
				try:
					txt_xbrl_handle = open(txt_name)
					txt_xbrl_holder = clean_txt_xbrl.clean(txt_xbrl_handle)
				except:
					print "died xbrl cleaning "+txt_name

				xbrl = 0
				if len(txt_xbrl_holder) != 0:
					xbrl = 1
					xbrl_base_fn = "/media/data/investments/data/edgar/forms/rss/loaded/xbrl/"
					xbrl_base_fn = xbrl_base_fn +file_date.replace("-","")+"/"+cik+"/"
					call(["mkdir","-p",xbrl_base_fn[:-1]])
					xbrl_fn = xbrl_base_fn + basename +"_"+period+"_"+filing_ts+".xbrl"
					call(["rm", "-rf", xbrl_fn])
					print "writing xbrl to: "+xbrl_fn								
					xbrl_handle = open(xbrl_fn,'w')
					for row in txt_xbrl_holder:
						xbrl_handle.write(row)
					xbrl_handle.close()
					statinfo = os.stat(xbrl_fn)
					print "xbrl_fn stat:"+str(statinfo.st_size)
					if statinfo.st_size == 0:
						print "Dying because zero byte cleaned xbrl"
						sys.exit(0)
				

				print str(time.time() - t0), ": PMB XBRL PULL"
				### /XBRL ###

				### HTML ###
				t0 = time.time()

				try:
					txt_handle = open(txt_name)
					txt_holder = clean_txt_html.clean(txt_handle)
				except:
					print "died html cleaning:"+txt_name

				html_base_fn = "/media/data/investments/data/edgar/forms/rss/loaded/html/"
				html_base_fn = html_base_fn +file_date.replace("-","")+"/"+cik+"/"
				call(["mkdir","-p",html_base_fn[:-1]])
				html_fn = html_base_fn + basename +"_"+period+"_"+filing_ts+".html"
				call(["rm", "-rf", html_fn])
				print "writing html to: "+html_fn								
				html_handle = open(html_fn,'w')
				for row in txt_holder:
					html_handle.write(row)
				html_handle.close()
				html_link = txt_url	

				print str(time.time() - t0), ": PMB HTML PULL"
				### /HTML ###



				try:
					cursor.execute("insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`,`html_link`,`status`, `type`) values ("+str(cik)+",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\""+html_fn+"\",\""+html_link+"\",\"S\",\"eod\")")
					conn.commit()
					cursor.execute("select eh_sk from extract_history order by eh_sk desc limit 1")
					eh_sk = cursor.fetchone()[0]

				except cursor.Error, e:
					try:   
						e.args[1].find("Duplicate")
					except:
						print "Error %d: %s" % (e.args[0],e.args[1])
						print "Failed to insert extract history value: "+str(cik)
					continue


				t0 = time.time()
			        if html_fn != "none":
					try:
						print "html_load_gaap.html_load("+name, cik, file_date, form, symbol, eh_sk
						#html_result = html_load_gaap.html_load(name, cik, file_date, form, symbol, eh_sk)
						html_result = html_load_gaap.html_load(name, cik, file_date, form, symbol, eh_sk, html_fn)
						print "html loaded"
					except:
						pass
				print str(time.time() - t0), ": PMB HTML LOAD"


				t0 = time.time()
				try:
					file = xbrl_fn
					cleansed_file = cleanse.cleanse(file,symbol)	
					print "cleansed file = "+cleansed_file
					statinfo = os.stat(cleansed_file)
					print "cleansed_fn stat:"+str(statinfo.st_size)
					loaded_fn = loaded_path + basename+"_p"+period+"_"+file_date+".xbrl"
					fn = cleansed_file[cleansed_file.rindex("/")+1:]
					error_fn = error_path + basename
					print "xbrl_load_quarter.xbrl_load "+cleansed_file, name, cik, file_date, form, symbol, eh_sk
					result = xbrl_load_quarter.xbrl_load(cleansed_file, name, cik, file_date, form, symbol, eh_sk)
					if result == 0:
						print "Successfully loaded xbrl file "+file  
						print "Moving xbrl_fn to: "+loaded_fn
						shutil.move(file,loaded_fn)
					else:
						print "Rss says period is "+period
						print "Error! Moving to: "+error_fn
						company_sk =  -1
						shutil.move(file,error_fn)
						try:
							print "Inserting error into insert extract history value:"
							cursor.execute("update extract_history set status = \"E\" where eh_sk = "+str(eh_sk))
							conn.commit()

						except cursor.Error, e:
							try:   
								e.args[1].find("Duplicate")
							except:
								print "Error %d: %s" % (e.args[0],e.args[1])
								print "Failed to insert extract history value: "+str(cik)



				except:
					print "xbrl fail for: "+name
				print str(time.time() - t0), ": PMB XBRL LOAD"


				try:
					conn.commit()
					print "select company_sk from company where cik = "+cik
					cursor.execute('select company_sk from company where cik != "FAILURE" and cast(cik as unsigned) = '+cik)
					company_sk = cursor.fetchone()[0]
					print "company_sk = "+str(company_sk)


				except:
					pass
					# Should I try to create a company_sk here?


				t0 = time.time()
				try:
					print "fulfilling html"
					fulfill_html.fulfill(file_date,0,0,form,company_sk,eh_sk,symbol,exchange,filing_ts)
					print "html fulfill complete"
				except:
					print "html fulfill failed"
				print str(time.time() - t0), ": PMB HTML FULFILL"


				t0 = time.time()
				try:

					print "fulfilling raw"
					print "date = "+date
					print "file_date = "+file_date
					fulfill_raw.fulfill_raw(file_date,0,0,form,company_sk,eh_sk,"","",symbol,exchange,filing_ts)
					print "post raw"
				except:
					print "raw fulfill failed"
				print str(time.time() - t0), ": PMB XBRL FULFILL"

				t0 = time.time()
				try:		
					print "Attempting to fulfill id (pre validation) raw and html"
					print " fulfill_id.fulfill(\""+file_date+"\",0,0,\""+str(form)+"\","+str(company_sk)+","+str(eh_sk)+")"
					num_companies = fulfill_id.fulfill(file_date,0,0,form,company_sk,eh_sk,"","",symbol,exchange,filing_ts)
				except:
					print "Ins fulfill failed"
				print str(time.time() - t0), ": PMB ID  FULFILL"

			if symbol == "LUB":
				sys.exit(0)
	else:
		continue

idx_handle.close()


#if not os.path.exists(bkp_path+"eod_"+date+".tar.gz"):

#call(["cp", "-r", "/media/data/investments/data/edgar/forms/eod/form_bkp/eod_"+date+".tar.gz", "/media/data/investments/data/edgar/forms/eod/form_bkp/eod_"+date+".tar.gz_bkp"])
#print "Archiving downloaded forms"

#call(["tar", "-czf", "/media/data/investments/data/edgar/forms/eod/form_bkp/eod_"+date+".tar.gz", temp_path])

call(["rm", "-rf", temp_path])
#call(["gzip","-f", idx_name])

cursor.close()
conn.commit()
conn.close()

#os.remove("/tmp/pull_run")


