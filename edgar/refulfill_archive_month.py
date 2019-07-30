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
import html_load_gaap
import cleanse
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

                master = retain[0]
                master_form = master[0]
                local_master_form = master[1]
                """
                print "master local = "+local_master_form
                print "master = "+master_form

                # Un comment me in test
                #result = html_load_gaap.html_load(local_master_form, name, cik, date, form, symbol, eh_sk)
                print "calling html_load"
                print " html_load_gaap.html_load("+local_master_form+", "+name+", "+str(cik)+", "+str(date)+", "+str(form)+", "+str(symbol)+", "+str(eh_sk)+")"
                """

                return(master_form,local_master_form)
        except:
                return("none","none")


#id = hashlib.md5(url + title).hexdigest()
conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()




# Every 10 minutes, check
#url = 'http://www.sec.gov/Archives/edgar/xbrlrss.all.xml'

# January
#url = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-2013-01.xml'

# Feb 
#url = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-2013-02.xml'


year = sys.argv[1]
month = sys.argv[2]

url = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-'+year+'-'+month+'.xml'

print "url = "+url



d = feedparser.parse(url)


# It will have 200 entries



path = "/media/data/investments/data/edgar/forms/rss/"
temp_path = "/media/data/investments/data/edgar/forms/temp/"
loaded_path = "/media/data/investments/data/edgar/forms/rss/loaded/"
error_path = "/media/data/investments/data/edgar/forms/rss/error/"
date = str(unicode(datetime.today())[:10]).replace("-","")
cursor.execute(" select date_id from dates where date = \""+str(date)+"\"")
row = cursor.fetchone()
#date_id = row[0]
count = 0

for feed in d['entries']:
	print "here"
        if  os.path.isfile("/home/peter/work/edgar/run") == False:
                        sys.exit(0)
        path = "/media/data/investments/data/parsed/extract/"+year+"/"
	
	form =  feed['edgar_formtype']
	print "Processing form "+str(form)
	if feed['edgar_formtype'] == '10-Q' or feed['edgar_formtype'] == '10-K' or feed['edgar_formtype'][0:3] == '8-K': 

		url = feed['id']
		file =  str(url[url.rindex("/")+1:])
		#name = feed['description']
		name = feed['edgar_companyname']
		fn_name = name.replace(" ","_").replace("/","-").replace(".","").replace("&","AND").replace(",","").replace("-","")

		new_file = 0
		cik = ""
		cik = feed['edgar_ciknumber']
		link = feed['link']
		period = feed['edgar_period']
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
			file_date = str(datetime.fromtimestamp(time.mktime(file_time)).date())
		except:
			file_date = str(datetime.today().date()) 
			


                unparsed_date = feed['edgar_filingdate'] # MM/DD/YYYY
                d = datetime.strptime(unparsed_date, '%m/%d/%Y')
                file_date = d.strftime('%Y-%m-%d')

		cursor.execute(" select date_id from dates where date = \""+str(file_date)+"\"")
		row = cursor.fetchone()
		date_id = row[0]

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


			print "new file "+name

			#loaded_path = path +fn_name+"/"+file_date+"/"+period+"/"+form+"/"
			loaded_path = path +fn_name+"/"+file_date+"/"
			loaded_path_temp = loaded_path+"temp/"
	                basename = fn_name+"_"+form.replace(" ","_")+"_"+period+"_"+str(int(cik))
                        loaded_fn = loaded_path + basename

	

			print "name = "+name,form
			#zip_name = temp_path + name.replace(" ","").replace('/',"").replace('\',"")+".zip"
			#zip_name = temp_path + name.replace(" ","").replace('/',"").replace('\\',"")+".zip"

			zip_name = loaded_path +"/"+basename+".zip"
			call(["mkdir","-p",loaded_path[:-1]])
			call(["mkdir","-p",loaded_path_temp[:-1]])
		        if  os.path.isfile(zip_name) == False:
				call(["wget", "-q", "-O", zip_name, url])
				call(["unzip","-q", "-d",loaded_path_temp, zip_name])
				


			if form == "10-K" or form == "10-Q":

 			 for file in sorted(glob.glob( os.path.join(loaded_path_temp, '*[0-9].xml') )):
				# load the xbrl file
				print "Loading :"+file, file_date	
				cleansed_file = cleanse.cleanse(file,symbol)	
				loaded_fn = loaded_fn.replace(".xml","_"+form+".xml")
				html_base_fn = loaded_path + "html/"
				html_extension_fn = basename+".html"

				fn = cleansed_file[cleansed_file.rindex("/")+1:]
				error_fn = error_path + basename


				# Pull down the html 
				print "pulling link: "+link
				html_link, html_fn = pull_html(symbol,form,cik,file_date,loaded_path,html_base_fn,html_extension_fn,link)



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
						html_result = html_load_gaap.html_load(html_fn, name, cik, file_date, form, symbol, eh_sk)
					except:
						pass


				result = xbrl_load_quarter.xbrl_load(cleansed_file, name, cik, file_date, form, symbol, eh_sk)


				if result == 0:
					print "Success!  Moving to: "+loaded_fn
					shutil.move(file,loaded_fn)
					# Its been loaded, look for the company_sk
					conn.commit()
					print "select company_sk from company where cik = \""+cik+"\""
					cursor.execute("select company_sk from company where cik = \""+cik+"\"")
					company_sk = cursor.fetchone()[0]
		



					print "fulfilling raw and html"
#PMB FIGURE OUT WHERE THESE ARE LANDING THEIR DATA..  MANIPULATE?
					print "html fulfill complete"
					fulfill_raw.fulfill_raw(file_date,0,0,form,company_sk,eh_sk,loaded_path,basename+"_parsed.csv")


					print "Attempting to fulfill id (pre validation) raw and html"
					print " fulfill_id.fulfill(\""+file_date+"\",0,1,\""+str(form)+"\","+str(company_sk)+","+str(form)+")"
					num_companies = fulfill_id.fulfill(file_date,1,1,form,company_sk,eh_sk,loaded_path,basename+"_instrumental.csv")

					sys.exit(0)					
					


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



			print "Done with "+name
			print


cursor.close()
conn.commit()
conn.close()


