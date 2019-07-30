#!/usr/bin/python

#
# Usage:

import utility
import sys
import time
from datetime import datetime
import os
import os.path
import glob
from subprocess import call
import feedparser
import hashlib
import MySQLdb
import get_edgar_cik
import shutil
import filecmp
#import selenium_edgar
import fulfill_id as fulfill_id
import fulfill_raw as fulfill_raw
import fulfill_html as fulfill_html
import table_reader as table_reader
import html_load_gaap as html_load_gaap
import get_cik
import tweet
import clean_txt_html
import clean_txt_xbrl
import xbrl_load_quarter


conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()


filing = {}

# First check all the filings

if os.path.exists("/tmp/online_run"):
        print "online still running"
        sys.exit(0)

block = open("/tmp/online_run",'w')
block.close()

try:
	edgar_ciks = get_edgar_cik.get_cik()
except:
	print "Died pulling edgar cik info?!"
        sys.exit(0)



write = 0
temp_path = "/media/data/investments/temp/"
temp_htm = temp_path+"list.htm"
temp_dump = temp_path+"list.dump"
call(["wget", "-q", "-O", temp_htm, "http://yahoo.brand.edgar-online.com/"])
lf = open(temp_dump,"w")
call(["lynx", "-dump", temp_htm], stdout=lf)
lf.close()
f = open(temp_dump)
key_store = 0
file_date = str(datetime.today().date())
date = str(datetime.today().date()).replace("-","")

date_id = str(utility.get_date_id(cursor,file_date))


# BUILD FILING DICT ( key => form, name, period, link )

for record in f:
	if record.find("Results 1") != -1:
		break
	if write == 1:
		try:
			#print record 
			# key_store is a buffer to store the key in case the period is on the following line, it is not set if the period is on the line w/ the filing

			if key_store == 0 or record.strip()[0] == "[":
				key = record[record.index("[")+1:record.index("]")]
				key_store = 0
			else:
				key_store = 0

			form = record[record.index("]")+1:].split(" ")[0]
			company_1 = record.split(form)[1]
			company_2 = company_1[:company_1.index(":")].strip()
			company =  company_2[:company_2.rindex(" ")].strip()
			#print form, company
			#period = record.split("M (")[1].replace(")","")
			#period = record.strip()[-9:].replace(")","")
			try:
				period = record[record.rindex("(")+1:record.rindex(")")]
			except:
				key_store = key
			if period == "":
				key_store = key
			filing[key] = [form, company,period]
			
		except:
			continue
	if record.find("Company") != -1 and record.find("Filer") != -1:
		write = 1

f.close()
write = 0
f = open(temp_dump)
for record in f:
	if record.find("Visible links") != -1:
		write = 1
	if write == 1:
		key = record.strip().split(".")[0]
		if key in filing.keys():
			try:
				filing[record.strip().split(".")[0]].append("http"+record.strip().split(" http")[1])
			except:
				try:
					record = record.replace('file://localhost/','http://yahoo.brand.edgar-online.com/')
					filing[record.strip().split(".")[0]].append("http"+record.strip().split(" http")[1])

				except:
					pass

f.close()




# PSUDEO CODE

# for all 8 - K, 10-K, and 10-Q,
	# if the NAME doesn't match in the extract_history table for today for this form 
		# pull back the filing and check the cik
		# if not in the edgar list,  
			# load to extract history
			# get the symbol from filing
			# go to the yahoo recent filings
			# get the most recent filing link
			# construct the edgar txt link
			# download it, clean it, load it
		# if in edgar list:
			#insert name into extract history
		

for item in filing.keys():
	#print filing[item]
	form = filing[item][0]
	name = filing[item][1]
	period = filing[item][2]
	link = filing[item][3]

		

	if form == "8-K" or form == "10-K" or form == "10-Q":

		try:
			print ""
			print "=========================="
			print "=      NEW FILING        ="
			print "=========================="
			print ""
				
			print name, form


			## GET THE PERIOD

			try:
				d = datetime.strptime(period, "%m/%d/%y")
				period = d.strftime("%Y%m%d")
			except:
				print "couldn't deal with period"
				print filing[item]
				# Insert row to eh to skip in the future
				cursor.execute("insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`,`html_link`,`status`) values (\""+str(0)+"\",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\"\",\"\",\"N\")")
				conn.commit()
				continue


			## CHECK IF I ALREADY KNOW ABOUT YOU 

			new_file = 0
			result = None
			try:
				cursor.execute(" select eh_sk from extract_history where name = \""+str(name)+"\" and form = \""+form+"\" and date_id = "+date_id)
				#print " select eh_sk from extract_history where name = \""+str(name)+"\" and form = \""+form+"\" and date_id = "+date_id
				result = cursor.fetchone()[0]
			except:
				result = None
			if result == None:
				#  This means that I didn't find this filing
				new_file = 1

			if new_file == 0:
				print "Already loaded"
	
				#  Not a new file
				continue


			# PULL BACK ONLINE FILING AND GRAB THE CIK

			temp_htm = temp_path+"filing.htm"
			temp_dump = temp_path+"filing.dump"
			print "pulling "+temp_htm+" to "+temp_dump
			call(["wget", "-q", "-O", temp_htm, link])
			lf = open(temp_dump,"w")
			call(["lynx", "-dump", temp_htm], stdout=lf)
			lf.close()
			filing_handle = open(temp_dump)
			bad_row = 0
			symbol = ""
			try:
				for row in filing_handle:
					if row.strip()[0:3] == "CIK":
						try:
							cik = row.strip().split("]")[1]	
						except:
							bad_row = 1
					if row.strip()[0:7] == "Company:":
						try:
							symbol = row.strip()[row.strip().rindex("(")+1:-1]
						except:
							print "No symbol for "+name
							try:
								cursor.execute("insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`,`html_link`,`status`) values (\""+str(cik)+"\",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\"\",\"\",\"N\")")
								conn.commit()
							except:
								try:
									cursor.execute("insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`,`html_link`,`status`) values (\""+str(0)+"\",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\"\",\"\",\"N\")")
									conn.commit()
								except:
									pass
							bad_row = 1
			except:
				bad_row = 1



			# REMOVE ME FOR HISTORY EXTRACT
			cursor.execute(" select symbol, exchange from symbol where current = 1 and cik = \""+str(cik)+"\"")
			try:
				result = cursor.fetchone()
				table_symbol = result[0]
				exchange = result[1]
			except:
				table_symbol = "NA"
				exchange = "NA"

			if symbol.find(".") != -1 or bad_row == 1 or table_symbol == "NA":
				try:
					print "symbol = "+symbol
					print "table_symbol = "+table_symbol
				except:
					print "no symbol"
				try:
					print "cik = "+str(cik)
				except:
					print "no cik"
				continue

			if table_symbol != symbol:
				print "name = "+name
				print "table_symbol = "+table_symbol
				print "symbol = "+symbol

					
			## NOW THAT I HAVE THE CIK, CHECK AGAIN TO SEE IF I ALREADY KNOW ABOUT YOU	

			try:
				cursor.execute(" select eh_sk from extract_history where cik = \""+str(cik)+"\" and form = \""+form+"\" and date_id = "+date_id)
				result = cursor.fetchone()[0]
			except:
				result = None


			if cik in edgar_ciks or result != None:
				# Insert row to eh to skip in the future
				print "Edgar knows about me: "+name
				#cursor.execute("insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`,`html_link`,`status`) values (\""+str(cik)+"\",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\"\",\"\",\"N\")")
				#conn.commit()
				continue


			## QUERY YAHOO TO GET THE PATH DETAILS ON THIS FILING 	


			print "pulling recent filings for:",symbol
			temp_htm = temp_path+"recent.htm"
			temp_dump = temp_path+"recent.dump"
			recent_link = "http://finance.yahoo.com/q/sec?s="+symbol+"+SEC+Filings"
			try:
				call(["wget", "-q", "-O", temp_htm, recent_link])
				lf = open(temp_dump,"w")
				call(["lynx", "-dump", temp_htm], stdout=lf)
				lf.close()
			except:
				print "failed to pull down recent filings: "+recent_link, temp_htm
				cursor.execute("insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`,`html_link`,`status`) values (\""+str(cik)+"\",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\"\",\"\",\"N\")")
				conn.commit()
				continue


			recent_handle = open(temp_dump)
			recent_keys = {}
			for row in recent_handle:
				if row.find("Full Filing at EDGAR Online") != -1:
					key = row[row.rindex("[")+1:row.rindex("]")]
			recent_handle.close()
			recent_handle = open(temp_dump)

			try:
				write = 0
				for record in recent_handle:
					if record.find("Visible links") != -1:
						write = 1
					if write == 1:
						if record.find(key+". http") != -1:
							recent_txt_url = "http"+record.strip().split(" http")[1]
				recent_handle.close()
			except:
				print "failed to find link in : "+temp_dump
				try:
					print "key = "+key
				except:
					pass
				cursor.execute("insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`,`html_link`,`status`) values (\""+str(cik)+"\",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\"\",\"\",\"N\")")
				conn.commit()
				continue

			try:
				print "found:", recent_txt_url
			except:
				print "recent_txt_url is not set for: "+name
				
			try:
				int_cik =  recent_txt_url.split("-")[-4]
				folder =  recent_txt_url.split("-")[-3]
				type =  recent_txt_url.split("-")[-2]
				id  =  recent_txt_url.split("-")[-1].split("&")[0]
				fn_name = utility.clean_name(name)
				basename = fn_name.replace(" ","_").replace('/',"")+"_"+form.replace(" ","_").replace('/',"")
				filing_temp_path = "/media/data/investments/data/edgar/forms/temp/"
				txt_name = temp_path +basename+".txt"
				txt_url =  "http://www.sec.gov/Archives/edgar/data/"+int_cik+"/"+folder+type+id+"/"+folder+"-"+type+"-"+id+".txt"
				print "looking for:",txt_url
			except:
				print "failed getting information out of: "+recent_txt_url



			## PULL THE FILING FROM THE SEC SERVERS

			call(["wget", "-q", "-O", txt_name, txt_url])
			print "pulled data to "+txt_name
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
				call(["mkdir","-p",xbrl_base_fn[:-1]])
				print "online created", xbrl_base_fn
				xbrl_fn = xbrl_base_fn + basename +"_"+form+"_"+period+".xbrl"
				xbrl_handle = open(xbrl_fn,'w')
				for row in txt_xbrl_holder:
					xbrl_handle.write(row)
				xbrl_handle.close()

			try:
				txt_html_handle = open(txt_name)
				txt_html_holder = clean_txt_html.clean(txt_html_handle)
			except:
				print "died html cleaning "+txt_name
			html_base_fn = "/media/data/investments/data/edgar/forms/rss/loaded/html/"
			html_base_fn = html_base_fn +date+"/"+cik+"/"
			call(["mkdir","-p",html_base_fn[:-1]])
			print "online created", html_base_fn
			html_fn = html_base_fn + basename +"_"+form+"_"+period+".html"
			html_handle = open(html_fn,'w')
			for row in txt_html_holder:
				html_handle.write(row)
			html_handle.close()

			html_link = txt_url

			# LOAD IT

			try:
				cursor.execute("insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`,`html_link`,`status`) values (\""+str(cik)+"\",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\""+html_fn+"\",\"\",\"O\")")
				conn.commit()
				cursor.execute("select eh_sk,insert_ts from extract_history order by eh_sk desc limit 1")
				row = cursor.fetchone()
				eh_sk = row[0]
				insert_ts = row[1]
				print "Successful insert into extract_history for "+name+" : "+str(symbol), str(eh_sk)

				try:
					cursor.execute("insert into filing_trade (eh_sk,insert_ts,date_id,state,symbol, exchange) values ("+str(eh_sk)+",'"+str(insert_ts)+"',"+str(date_id)+",0,'" +str(symbol)+"','"+str(exchange)+"')")
					conn.commit()
					print "Successful loaded to filing_trade for "+name+" : "+str(symbol), str(eh_sk)
				except:
					print "Filing Trade insert FAILED!!!!!"
					try:
						print "insert into filing_trade (eh_sk,insert_ts,date_id,state,symbol, exchange) values ("+str(eh_sk)+",'"+str(insert_ts)+"',"+str(date_id)+",0,'" +str(symbol)+"','"+str(exchange)+"')"
					except:
						print "I can't even print the insert statement!!!"


				

			except cursor.Error, e:
				try:
					e.args[1].find("Duplicate")
				except:
					print "Error %d: %s" % (e.args[0],e.args[1])
					print "Failed to insert extract history value: "+str(cik)
					continue
			




			try:
				cursor.execute(" select company_sk from company where cik = "+str(cik))
				row = cursor.fetchone()
				company_sk = row[0]

			except:
				try:
					print "inserting company information: "
					print "insert into company (`name`, `cik`, `industry`, `industry_id`, `corp_state`, `address_line_1`, `address_line_2`, `city`, `state`, `zip`) values ("+",".join(map(str,[company, cik, industry, industry_id, corp_state, address_line_1, address_line_2, city, state, zip]))+")"
					cursor.execute ("insert into company (`name`, `cik`, `industry`, `industry_id`, `corp_state`, `address_line_1`, `address_line_2`, `city`, `state`, `zip`) values ("+",".join(map(str,[name, cik, '', '', '', '', '', '', '', '']))+")")
					conn.commit()
					cursor.execute(" select company_sk from company where cik = "+str(cik))
					row = cursor.fetchone()
					company_sk = row[0]

				except cursor.Error, e:
					try:
						e.args[1].find("Duplicate")
					except:
						print "Error %d: %s" % (e.args[0],e.args[1])
						print "failed to insert company info: "+",".join(map(str,[company, cik, industry, industry_id, corp_state, address_line_1, address_line_2, city, state, zip]))
					continue





			# try to parse and load it
			try:
				print "Loading HTML"
				print "html_load_gaap.html_load("+name, str(cik), file_date, form, symbol, str(eh_sk)
				html_result = html_load_gaap.html_load(name, str(cik), file_date, form, symbol, str(eh_sk))
				print 'loaded!'
			except:
				print "Died in HTML Load for "+name
				print "No PARSED data for "+name
				#break
				
			try:
				print "xbrl = "+str(xbrl)
				print "txt_name "+txt_name
				if xbrl == 1:	
					clean_xbrl_fn = cleanse.cleanse(xbrl_fn,symbol)
					result = xbrl_load_quarter.xbrl_load(clean_xbrl_fn, name, cik, file_date, form, symbol, str(eh_sk))		
				else: 
					print "no xbrl for "+txt_name
			except:
				print "Died in XBRL Load for "+name
				break	

			# try to fulfill it
			try:
				print "fulfilling!"
				fulfill_html.fulfill(file_date,0,0,form,company_sk,eh_sk)
			except:
				print "html fulfill failed for  "+file_date,form,company_sk,eh_sk
			try:
				fulfill_raw.fulfill_raw(file_date,0,0,form,company_sk,eh_sk,"","")
			except:
				print "raw fulfill failed for  "+file_date,form,company_sk,eh_sk
			try:	
				print "Attempting to fulfill id (pre validation) raw and html" 
                                print " fulfill_id.py \""+file_date+"\" \""+str(form)+"\" "+str(company_sk)+" "+str(eh_sk)+")"
                                num_companies = fulfill_id.fulfill(file_date,form,company_sk,eh_sk) 

				if num_companies == "1":
					print "insert into validation (company_sk, form, status, date_id, stamp_created,stamp_updated) values ("+str(company_sk)+",\""+form+"\",\"N\", "+str(date_id)+",null,null"
					cursor.execute("insert into validation (company_sk, form, status, date_id, stamp_created,stamp_updated,eh_sk) values ("+str(company_sk)+",\""+form+"\",\"N\", "+str(date_id)+",null,null,"+str(eh_sk)+")")
					conn.commit()
			except:
				print "id fulfill failed for  "+file_date,form,company_sk,eh_sk



			if symbol != "NA":
				try:
					tweet.tweet(name, exchange, symbol, form)  #PMB UNCOMMENT ME
					pass
				except:
					print "no tweets!"


		except:
			print "died in the outer ring for: "+str(filing[item])
			try:
				cursor.execute("insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`,`html_link`,`status`) values (\""+str(cik)+"\",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\"\",\"\",\"N\")")
				conn.commit()
				break
			except:
				break

		print ""
		print "=========================="
		print "=      FILING ENDED      ="
		print "=========================="
		print ""


			
	

conn.commit()
cursor.close()
conn.close()
os.remove("/tmp/online_run")

