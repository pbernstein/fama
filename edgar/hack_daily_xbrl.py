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
import xbrl_load_quarter
import html_load
import cleanse
import send_generic_email_attachment as send_email
import fulfill_id as fulfill_id
import fulfill_raw as fulfill_raw
import fulfill_html as fulfill_html
import table_reader as table_reader
import tweet




def pull_html(symbol, form,cik,date,temp_path,html_base_fn, html_extension_fn,link):

	# look for any instance of "*.htm"
	# between
		# Document Format Files
	# and
		# Data Files
	# pull it and land it to a meaningful CIK name in a directory rss/loaded/html/date/cik/
	html_base_fn = html_base_fn +date+"/"+cik+"/"
	retain = []
	#print "creating "+html_base_fn
	call(["mkdir","-p",html_base_fn[:-1]])

	try:
		call(["wget", "-q", "-O", temp_path+"index.htm", link])
		lf = open(temp_path+"index.dump","w")
		call(["lynx", "-dump", temp_path+"index.htm"], stdout=lf)
		lf.close()
		f = open(temp_path+"index.dump")
		htm_link = ""
		next = 1
		for line in f:
	
			if line.find("Document Format Files") != -1:
				next = 0
			if line.find("Data Files") != -1:
				next = 1
			if next == 1:
				continue
			
			html_fn_has_tables = ""
			if line.find(".htm") != -1:
				#print "found html filing"
				#htm_link = line[line.index('a href="')+8:line.rindex('"')]
				html_field = ""
				htm_link = ""
				for field in line.split(" "):
					if field.find(".htm") != -1:
						html_field = field.split("]")[1]
			
			
				if html_field != "":	
					fh  = open(temp_path+"index.htm")
					for h_line in fh:
						if h_line.find(html_field) != -1:
							htm_link = h_line[h_line.index('a href="')+8:h_line.rindex('"')]
					fh.close()
					
				if htm_link != "":		
					#print "found "+htm_link
					htm_link = "http://www.sec.gov"+htm_link
					htm_server_fn = htm_link[htm_link.rindex("/")+1:]
					html_fn = html_base_fn + htm_server_fn + "_"+html_extension_fn	
					html_fn.replace("/","_")
					#print "landing to "+html_fn
					if  os.path.isfile(html_fn) == False:
						call(["wget", "-q", "-O",html_fn, htm_link])
					try:
						#if table_reader.main(html_fn) != []:
						#	html_link_has_tables = htm_link
						#	html_fn_has_tables = html_fn
						hf = open(html_fn+".dump","w")
						call(["lynx","-dump",html_fn],stdout=hf)
						hf.close()
						result = call(["grep","-i","Commission File",html_fn+".dump"])
						if result == 0:
							try:
								new_html_fn = html_fn.replace(htm_server_fn,form.upper())
								shutil.move(html_fn,new_html_fn)
								retain.append([htm_link,new_html_fn])
							except:
								print "move fail"
						call(["rm",html_fn+".dump"])
							
					except:
						print "died somewhere!"
						pass
					#print "Pulled!"
			
					
		f.close()
	except:
		print "died pulling html!"
		pass

	call(["rm", temp_path+"index.htm"])
	call(["rm", temp_path+"index.dump"])
	try:
		master = retain.pop()
		master_form = master[0]
		local_master_form = master[1]
		print "master local = "+local_master_form
		print "master = "+master_form

		# Un comment me in test
		result = html_load.html_load(local_master_form, name, cik, date, form, symbol, eh_sk)

		return(master_form)
	except:
		return("none")


#id = hashlib.md5(url + title).hexdigest()
conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()




# Every 10 minutes, check
#url = 'http://www.sec.gov/Archives/edgar/xbrlrss.all.xml'

# January
#url = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-2013-01.xml'

# Feb 
url = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-2013-02.xml'



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
	
	form =  feed['edgar_formtype']
	print "Processing form "+str(form)
	if feed['edgar_formtype'] == '10-Q' or feed['edgar_formtype'] == '10-K' or feed['edgar_formtype'][0:3] == '8-K': 

		url = feed['id']
		file =  str(url[url.rindex("/")+1:])
		#name = feed['description']
		name = feed['edgar_companyname']
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
		period = feed['edgar_period']
		try:
			file_date = str(datetime.fromtimestamp(time.mktime(file_time)).date())
		except:
			file_date = str(datetime.today().date()) 


                unparsed_date = feed['edgar_filingdate'] # MM/DD/YYYY
                d = datetime.strptime(unparsed_date, '%m/%d/%Y')
                file_date = d.strftime('%Y-%m-%d')

		try:
       			cursor.execute(" select eh_sk from extract_history where cik = \""+str(cik)+"\" and period = \""+str(period)+"\" and form = \""+form+"\"")
		        result = cursor.fetchone()[0]
			try:
				#print "result = "+str(result)
				test = result
			except:
				result = None
			if result == None:
				new_file = 1
				#  This means that I didn't find this period for this company
				#  Therefore, i load the file
		except:
			new_file = 1
			#  This means that I didn't find this CIK in the table, which means i'm not aware of this company and I should load the file, also, i need to figure out the company sk :)



		# REMOVE ME FOR HISTORY EXTRACT 
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
	
		if new_file == 1:




			

			print "name = "+name
			#zip_name = temp_path + name.replace(" ","").replace('/',"").replace('\',"")+".zip"
			zip_name = temp_path + name.replace(" ","").replace('/',"").replace('\\',"")+".zip"
			print "url = "+url

			call(["rm","-r", temp_path[:-1]])
			call(["mkdir","-p",temp_path[:-1]])
			call(["wget", "-q", "-O", zip_name, url])
			call(["unzip","-q", "-d",temp_path, zip_name])


			# move the pull down html part to here
			if form[0:3] == "8-K":
				basename = name.replace(" ","_")+"_"+form.replace(" ","_")
				loaded_fn = loaded_path + basename
				loaded_fn = loaded_fn.replace(".xml","_"+form+".xml")
				html_base_fn = loaded_path + "html/"
				html_extension_fn = basename+".html"
				# Pull down the html 
				try:
					print "pulling link: "+link
					htm_link = pull_html(symbol,form,cik,file_date,temp_path,html_base_fn,html_extension_fn,link)
					try:
						print "Inserting into insert extract history value:"+htm_link
			#						print "insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`) values ("+str(cik)+",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\""+str(html_fn)+"\")"
						cursor.execute("insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`,`html_link`) values (\""+str(cik)+"\",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\"none\",\""+htm_link+"\")")
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



					try:

						fulfill_html.fulfill(file_date,0,0,form,company_sk,eh_sk)
						#Tweet about it
						#if symbol != "NA":
						#	try:
						#		tweet.tweet(name, exchange, symbol, form)
						#	except:
						#		"no tweets!"

					except:
						print "no html fulfill for you! "+company_sk, name, symbol, form


				except:
					pass



			if form == "10-K" or form == "10-Q":

 			 for file in sorted(glob.glob( os.path.join(temp_path, '*[0-9].xml') )):
				# load the xbrl file
				print "Loading :"+file, file_date	
				#cleansed_file = cleanse.cleanse(file,symbol)	
				basename = file[file.rindex("/")+1:]
				loaded_fn = loaded_path + basename 
				loaded_fn = loaded_fn.replace(".xml","_"+form+".xml")
				html_base_fn = loaded_path + "html/"
				html_extension_fn = basename+".html"
				html_fn = "none"

				#fn = cleansed_file[cleansed_file.rindex("/")+1:]
				error_fn = error_path + basename


				# Pull down the html 
				print "pulling link: "+link
				htm_link = pull_html(symbol, form,cik,file_date,temp_path,html_base_fn,html_extension_fn,link)


				try:
					print "Inserting into insert extract history value:"+htm_link
		#						print "insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`) values ("+str(cik)+",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\""+str(html_fn)+"\")"
					cursor.execute("insert into extract_history (`cik`,`name`,`period`,`form`,`date_id`,`html`,`html_link`) values (\""+str(cik)+"\",\""+name+"\", \""+period+"\", \""+str(form)+"\", "+str(date_id)+",\"none\",\""+htm_link+"\")")
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


			print "Done with "+name
			print
			#sys.exit(0)					


cursor.close()
conn.commit()
conn.close()


