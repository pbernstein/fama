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

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

# SET GLOBALS
conn = db.get_conn()
cursor = conn.cursor()





#url = 'http://www.sec.gov/Archives/edgar/xbrlrss.all.xml'

# January
#url = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-2013-01.xml'

# Feb 
#url = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-2013-02.xml'

month = sys.argv[1]
url = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-2013-'+str(month)+'.xml'

d = feedparser.parse(url)

# It will have 200 entries

path = "/media/data/investments/data/edgar/forms/rss/"
temp_path = "/media/data/investments/data/edgar/forms/temp/"
loaded_path = "/media/data/investments/data/edgar/forms/rss/loaded/"
error_path = "/media/data/investments/data/edgar/forms/rss/error/"
#date = str(unicode(datetime.today())[:10]).replace("-","")
count = 0

for feed in d['entries']:
	#if feed['edgar_formtype'] == '10-Q': # or feed['edgar_formtype'] == '10-K': 
	#if feed['edgar_formtype'] == '10-Q' or feed['edgar_formtype'] == '10-K': 
	
	form =  feed['edgar_formtype']
	print "Processing form "+str(form)
	if feed['edgar_formtype'] == '10-Q' or feed['edgar_formtype'] == '10-K' or feed['edgar_formtype'][0:3] == '8-K': 
		try:
			url = feed['id']
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
			unparsed_date = feed['edgar_filingdate'] # MM/DD/YYYY
			d = datetime.strptime(unparsed_date, '%m/%d/%Y')
			file_date = d.strftime('%Y-%m-%d')
			date = file_date.replace("-","")
			cursor.execute(" select date_id from dates where date = \""+str(file_date)+"\"")
			row = cursor.fetchone()
			date_id = row[0]
		except:
			pass
		

		try:
       			print "select eh_sk from extract_history where cik = \""+str(cik)+"\" and period = \""+str(period)+"\" and form = \""+form+"\""
       			cursor.execute(" select eh_sk from extract_history where cik = \""+str(cik)+"\" and period = \""+str(period)+"\" and form = \""+form+"\"")
		        result = cursor.fetchone()[0]
			try:
				#print "result = "+str(result)
				eh_sk = result
			except:
				result = None
			if result == None:
				new_file = 1
				#  This means that I didn't find this period for this company
				#  Therefore, i load the file
		except:
			new_file = 1
			#  This means that I didn't find this CIK in the table, which means i'm not aware of this company and I should load the file, also, i need to figure out the company sk :)



       		cursor.execute(" select symbol, exchange from symbol where start_date_id <= \""+str(date_id)+"\" and end_date_id > \""+str(date_id)+"\"   and cik = \""+str(cik)+"\"")
		try:
			result = cursor.fetchone()
			symbol = result[0]
			exchange = result[1]
		except:
			symbol = "NA"
			exchange = "NA"
			


		if new_file == 0:
			print "Skipping "+name+".  Already loaded!"
			continue
	
		#if new_file == 1:
		if 1 == 1:




			

			print "name = "+name
			basename = fn_name.replace(" ","_").replace('/',"")+"_"+form.replace(" ","_").replace('/',"")
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
                                xbrl_base_fn = xbrl_base_fn +date+"/"+cik+"/"
				call(["rm","-r", xbrl_base_fn[:-1]])
                                call(["mkdir","-p",xbrl_base_fn[:-1]])
                                #xbrl_fn = xbrl_base_fn + basename +"_"+period+".xbrl"
                                xbrl_fn = xbrl_base_fn + basename +".xbrl"
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
			html_base_fn = html_base_fn +date+"/"+cik+"/"
			call(["rm","-r", html_base_fn[:-1]])
			call(["mkdir","-p",html_base_fn[:-1]])
			#html_fn = html_base_fn + basename +"_"+date+"_"+period+".html"
			html_fn = html_base_fn + basename +".html"
			print "writing to: "+html_fn								
			html_handle = open(html_fn,'w')
			for row in txt_holder:
				html_handle.write(row)
			html_handle.close()
		
			html_link = txt_url	


					
			if form == "10-K" or form == "10-Q" or form == "8-K":

 			 	#for file in sorted(glob.glob( os.path.join(temp_path, '*[0-9].xml') )):
				# load the xbrl file
				#print "Loading :"+file, file_date	
				print "Loading :"+symbol, file_date	





				try:
					cursor.execute("insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`,`html_link`,`status`) values (\""+str(cik)+"\",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\""+html_fn+"\",\""+html_link+"\",\"S\")")
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


			        if html_fn != "none":
					try:
						html_result = html_load_gaap.html_load(name, cik, file_date, form, symbol, eh_sk)
						print "html loaded"
					except:
						pass


				try:
					file = xbrl_fn
					cleansed_file = cleanse.cleanse(file,symbol)	
					loaded_fn = loaded_path + basename +".xbrl"
					#loaded_fn = loaded_fn.replace(".xml","_"+form+".xml")
					fn = cleansed_file[cleansed_file.rindex("/")+1:]
					error_fn = error_path + basename
					result = xbrl_load_quarter.xbrl_load(cleansed_file, name, cik, file_date, form, symbol, eh_sk)
					if result == 0:
						print "Success!  Moving to: "+loaded_fn
						shutil.move(file,loaded_fn)
					else:
						print "Rss says period is "+period
						print "Error! Moving to: "+error_fn
						company_sk =  -1
						html_link, html_fn = pull_html(symbol,form,cik,file_date,temp_path,html_base_fn,html_extension_fn,link)
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
					fulfill_raw.fulfill_raw(file_date,0,0,form,company_sk,eh_sk,"","")
				except:
					print "raw fulfill failed"

				try:		
					print "Attempting to fulfill id (pre validation) raw and html"
					"""
					print " fulfill_id.fulfill(\""+file_date+"\",0,1,\""+str(form)+"\","+str(company_sk)+","+str(form)+")"
					
					num_companies = fulfill_id.fulfill(file_date,0,0,form,company_sk,eh_sk,"","")
					if num_companies == "1":
						print "insert into validation (company_sk, form, status, date_id, stamp_created,stamp_updated) values ("+str(company_sk)+",\""+form+"\",\"N\", "+str(date_id)+",null,null"
						cursor.execute("insert into validation (company_sk, form, status, date_id, stamp_created,stamp_updated,eh_sk) values ("+str(company_sk)+",\""+form+"\",\"N\", "+str(date_id)+",null,null,"+str(eh_sk)+")")
						conn.commit()
					"""


				except:
					print "Ins fulfill failed"
				try:
					#Tweet about it
	
					if symbol != "NA":
						try:
							#tweet.tweet(name, exchange, symbol, form)
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



