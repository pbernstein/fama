#!/usr/bin/python

#
# Usage:


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
import fulfill_id as fulfill_id
import fulfill_raw as fulfill_raw
import fulfill_html as fulfill_html
import table_reader as table_reader
import tweet
import clean_txt_html
import clean_txt_xbrl


conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()

if os.path.exists("/tmp/pull_run"):
	print "pull still running"
	sys.exit(0)

block = open("/tmp/pull_run",'w')
block.close()



url = 'http://www.sec.gov/Archives/edgar/xbrlrss.all.xml'

# January
#url = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-2013-01.xml'

# Feb
#url = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-2013-02.xml'



d = feedparser.parse(url)

# It will have 200 entries

path = "/media/data/investments/data/edgar/forms/rss/"
temp_path = "/media/data/investments/data/edgar/forms/temp/"
loaded_path = "/media/data/investments/data/edgar/forms/rss/loaded/"
error_path = "/media/data/investments/data/edgar/forms/rss/error/"
date = str(unicode(datetime.today())[:10]).replace("-","")
cursor.execute(" select date_id from dates where date = \""+str(date)+"\"")
row = cursor.fetchone()
date_id = row[0]
count = 0

for feed in d['entries']:
	#if feed['edgar_formtype'] == '10-Q': # or feed['edgar_formtype'] == '10-K':
	#if feed['edgar_formtype'] == '10-Q' or feed['edgar_formtype'] == '10-K':
	try:
		form =  feed['edgar_formtype']
	except:
		continue
	print "Processing form "+str(form)
	if feed['edgar_formtype'] == '10-Q' or feed['edgar_formtype'] == '10-K' or feed['edgar_formtype'][0:3] == '8-K':
		try:
			#url = feed['id']  # Edgar versioned
			url = feed['url']
			
		except:
			print "Bad feed[id]"
			try:
				for data in feed:
					print data+":", feed[data]
			except:
				pass
			continue
		txt_url = url.replace("-xbrl.zip",".txt")
		print "txt_url: "+txt_url
		file =  str(url[url.rindex("/")+1:])
		#name = feed['description']
		name = feed['edgar_companyname']
		#fn_name = name.replace(" ","_").replace("/","-").replace(".","").replace("&","AND").replace(",","").replace("-","")
		fn_name = utility.clean_name(name)
		new_file = 0
		cik = ""
		cik = feed['edgar_ciknumber']
		link = feed['link']
		#commision_number = feed['edgar_filenumber']

		if cik == "":
			print "No CIK!?!!?"
			print "Name = "+str(name)
			exit(1)
		#print "name = "+name
		#for i in feed:
		#	print i, feed[i]
		try:
			file_time = feed['published_parsed']
		except:
			file_time = datetime.now()
		try:
			period = feed['edgar_period']
		except:
			print "No Period!?"
			print "Bad feed[id]"
			try:
				for data in feed:
					print data+":", feed[data]
			except:
				pass
			continue
		try:
			file_date = str(datetime.fromtimestamp(time.mktime(file_time)).date())
		except:
			file_date = str(datetime.today().date())


                unparsed_date = feed['edgar_filingdate'] # MM/DD/YYYY
                d = datetime.strptime(unparsed_date, '%m/%d/%Y')
                file_date = d.strftime('%Y-%m-%d')

		try:
       			cursor.execute(" select eh_sk, status from extract_history where cik = \""+str(cik)+"\" and period = \""+str(period)+"\" and form = \""+form+"\"")
		        results = cursor.fetchall()
			try:
				#print "result = "+str(result)
				if len(results) == 0:
					result = None
				else:

					for result in results:
						if result[1] == "N" or result[1] == "O":
							new_file = 2
							eh_sk = result[0]
							break
			except:
				result = None
			if result == None:
				new_file = 1
				#  This means that I didn't find this period for this company
				#  Therefore, i load the file
		except:
			new_file = 1
			#  This means that I didn't find this CIK in the table, which means i'm not aware of this company and I should load the file, also, i need to figure out the company sk :)



       		cursor.execute(" select symbol, exchange from symbol where current = 1 and cik = \""+str(cik)+"\"")
		try:
			result = cursor.fetchone()
			symbol = result[0]
			exchange = result[1]
		except:
			symbol = "NA"
			exchange = "NA"



		if new_file == 0:
			print "Skipping "+name+".  Already loaded!"

		else:

			if new_file == 2:
	                        cursor.execute(" delete from extract_history where eh_sk = "+str(eh_sk))
                                cursor.execute(" delete from gaap_value where eh_sk = "+str(eh_sk))
                                cursor.execute(" delete from ins_value where eh_sk = "+str(eh_sk))
                                conn.commit()
			try:
				#cursor.execute("insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`,`html_link`,`status`) values (\""+str(cik)+"\",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\""+html_fn+"\",\""+html_link+"\",\"S\")")
				cursor.execute("insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`,`html_link`,`status`) values (\""+str(cik)+"\",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\""+""+"\",\""+""+"\",\"S\")")
				conn.commit()
				cursor.execute("select eh_sk, insert_ts from extract_history order by eh_sk desc limit 1")
				row = cursor.fetchone()
				eh_sk = row[0]
				insert_ts = row[1]
				
				#try:
				#	cursor.execute('insert into filing_trade (`eh_sk`,`state`) values ("'+str(eh_sk)+'","0")')
				#	conn.commit()
				#except:
				#	print "failed to insert to filing trade"

			except cursor.Error, e:
				try:
					e.args[1].find("Duplicate")
				except:
					print "Error %d: %s" % (e.args[0],e.args[1])
					print "Failed to insert extract history value: "+str(cik)
				continue

			if symbol == "NA":
				continue




			print "name = "+name
			basename = fn_name.replace(" ","_").replace('/',"")+"_"+form.replace(" ","_").replace('/',"")
			#zip_name = temp_path + name.replace(" ","").replace('/',"").replace('\',"")+".zip"
			#zip_name = temp_path + fn_name.replace(" ","").replace('/',"").replace('\\',"")+".zip"
			zip_name = temp_path +basename+".zip"
			txt_name = temp_path +basename+".txt"

			print "url = "+url

			call(["rm","-r", temp_path[:-1]])
			call(["mkdir","-p",temp_path[:-1]])
			#call(["wget", "-q", "-O", zip_name, url])
			#call(["unzip","-q", "-d",temp_path, zip_name])
			call(["wget", "-q", "-O", txt_name, txt_url])

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
				#PMB UPDATE 0917
                                xbrl_base_fn = xbrl_base_fn +file_date.replace("-","")+"/"+cik+"/"
                                call(["mkdir","-p",xbrl_base_fn[:-1]])
                                xbrl_fn = xbrl_base_fn + basename +"_"+period+".xbrl"
				print "writing to: "+xbrl_fn
                                xbrl_handle = open(xbrl_fn,'w')
                                for row in txt_xbrl_holder:
                                        xbrl_handle.write(row)
                                xbrl_handle.close()



			try:
				txt_handle = open(txt_name)
				txt_holder = clean_txt_html.clean(txt_handle)
			except:
				print "died html cleaning:"+txt_name

			html_base_fn = "/media/data/investments/data/edgar/forms/rss/loaded/html/"
			#PMB UPDATE 0917
			html_base_fn = html_base_fn +file_date.replace("-","")+"/"+cik+"/"
			call(["mkdir","-p",html_base_fn[:-1]])
			html_fn = html_base_fn + basename +"_"+period+".html"
			print "writing to: "+html_fn
			html_handle = open(html_fn,'w')
			for row in txt_holder:
				html_handle.write(row)
			html_handle.close()

			html_link = txt_url



			if form == "10-K" or form == "10-Q" or form == "8-K":

				###     Load to filing_trader
				try:    
					cursor.execute("insert into filing_trade (eh_sk,insert_ts,date_id,state,symbol, exchange) values ("+str(eh_sk)+",'"+str(insert_ts)+"',"+str(date_id)+",0,'" +str(symbol)+"','"+str(exchange)+"')")
					conn.commit()
				except:
					print "Filing Trade insert FAILED!!!!!"
					try:
						print "insert into filing_trade (eh_sk,insert_ts,date_id,state,symbol, exchange) values ("+str(eh_sk)+","+str(insert_ts)+","+str(date_id)+",0,'" +str(symbol)+"','"+str(exchange)+"')"
					except:
						print "I can't even print the insert statement!!!"
					

				###     Done!

 			 	#for file in sorted(glob.glob( os.path.join(temp_path, '*[0-9].xml') )):
				# load the xbrl file
				#print "Loading :"+file, file_date
				print "Loading :"+symbol, file_date






			        if html_fn != "none":
					try:
						html_result = html_load_gaap.html_load(name, cik, file_date, form, symbol, eh_sk)
						print "html loaded"
					except:
						pass


				try:
					file = xbrl_fn
					cleansed_file = cleanse.cleanse(file,symbol)
					loaded_fn = loaded_path + basename
					loaded_fn = loaded_fn.replace(".xml","_"+form+".xml")
					fn = cleansed_file[cleansed_file.rindex("/")+1:]
					error_fn = error_path + basename
					print "xbrl_load_quarter.xbrl_load("+cleansed_file, name, cik, file_date, form, symbol, eh_sk
					result = xbrl_load_quarter.xbrl_load(cleansed_file, name, cik, file_date, form, symbol, eh_sk)
					if result == 0:
						print "Success!  Moving to: "+loaded_fn
						shutil.move(file,loaded_fn)
					else:
						print "Rss says period is "+period
						print "Error! Moving to: "+error_fn
						company_sk =  -1
						#html_link, html_fn = pull_html(symbol,form,cik,file_date,temp_path,html_base_fn,html_extension_fn,link)
						shutil.move(file,error_fn)
						try:
							print "Inserting error into insert extract history value:"
							#cursor.execute("insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`,`html_link`,`status`) values (\""+str(cik)+"\",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\""+html_fn+"\",\""+html_link+"\",\"E\")")
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








					# Its been loaded, look for the company_sk
				try:
					conn.commit()
					print "select company_sk from company where cik = \""+cik+"\""
					cursor.execute("select company_sk from company where cik = \""+cik+"\"")
					company_sk = cursor.fetchone()[0]


				except:
					pass
					# Should I try to create a company_sk here?


				try:
					print "fulfilling html"
					fulfill_html.fulfill(file_date,0,0,form,company_sk,eh_sk)
					print "html fulfill complete"
				except:
					print "html fulfill failed"


				try:

					print "fulfilling raw"
					print "date = "+date
					print "file_date = "+file_date
					fulfill_raw.fulfill_raw(file_date,0,0,form,company_sk,eh_sk,"","")
					print "Fulfill Raw Success"
				except:
					print "raw fulfill failed"

				try:
					print "Attempting to fulfill id (pre validation) raw and html"
					print " fulfill_id.py \""+file_date+"\" \""+str(form)+"\" "+str(company_sk)+" "+str(eh_sk)+")"
					#num_companies = fulfill_id.fulfill(file_date,0,0,form,company_sk,eh_sk,"","")
					num_companies = fulfill_id.fulfill(file_date,form,company_sk,eh_sk)
					print "Fulfill ID Success"

					try:
							print "num companies = "+num_companies
					except:
							print "no num companies"
					"""
					if num_companies == "1":
						print "insert into validation (company_sk, form, status, date_id, stamp_created,stamp_updated) values ("+str(company_sk)+",\""+form+"\",\"N\", "+str(date_id)+",null,null"
						cursor.execute("insert into validation (company_sk, form, status, date_id, stamp_created,stamp_updated,eh_sk) values ("+str(company_sk)+",\""+form+"\",\"N\", "+str(date_id)+",null,null,"+str(eh_sk)+")")
						conn.commit()
					"""


				except:
					print "Ins fulfill failed"
				try:
					#Tweet about it

					if symbol != "NA" and new_file == 1:
						try:
							print "Tweeting"
							tweet.tweet(name, exchange, symbol, form)
							pass
							"""
							Make a seperate tweet  when a filing  has no "NR", send out
							<Company name> reports N in Cash
							<Company name> reports N in Assets
							<Company name> reports N in
							cursor.execute("select period, attribute, value from ins_value where date_id = "+file_date+," and form = '"+form+"' and company_sk = "+str(company_sk)+"
							tweet.tweet_data(name, exchange, symbol, form, attribute, value)
							"""
						except:
							print "no tweets!"

				except:
					pass






			print "Done with "+name
			print
			#sys.exit(0)


cursor.close()
conn.commit()
conn.close()

os.remove("/tmp/pull_run")


