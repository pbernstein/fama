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


def is_xbrl(file):
        f = open(file)
        xbrl = 0
        for record in f:
                if record.find("<us-gaap:") != -1:
                        xbrl = 1
                        break
        return xbrl




def pull_html( form,cik,date,temp_path,html_base_fn, html_extension_fn,link):

	# look for any instance of "*.htm"
	# between
		# Document Format Files
	# and
		# Data Files
	# pull it and land it to a meaningful CIK name in a directory rss/loaded/html/date/cik/
	print "start html_base_fn = "+html_base_fn
	html_base_fn = html_base_fn +date+"/"+cik+"/"
	html_base_fn = temp_path+"html/"
	print "pulling html to "+html_base_fn
	retain = []
	#print "creating "+html_base_fn
	call(["mkdir","-p",html_base_fn[:-1]])

	try:
		if  os.path.isfile(temp_path+"index.htm") == False:
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
		#result = html_load.html_load(local_master_form, name, cik, date, form, symbol, eh_sk)

		return(master_form)
	except:
		return("none")


#id = hashlib.md5(url + title).hexdigest()
conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()



year = sys.argv[1]
month = sys.argv[2]

# Every 10 minutes, check
#url = 'http://www.sec.gov/Archives/edgar/xbrlrss.all.xml'

# January
#url = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-2013-01.xml'

# Feb 
#url = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-2013-02.xml'


url = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-'+year+'-'+month+'.xml'



d = feedparser.parse(url)


# It will have 200 entries

date = str(unicode(datetime.today())[:10]).replace("-","")
cursor.execute(" select date_id from dates where date = \""+str(date)+"\"")
row = cursor.fetchone()
date_id = row[0]
count = 0

for feed in d['entries']:
	path = "/media/data/investments/data/edgar/forms/archive/"
	loaded_path = "/media/data/investments/data/edgar/forms/archive/loaded/"
	error_path = "/media/data/investments/data/edgar/forms/archive/error/"
	#if feed['edgar_formtype'] == '10-Q': # or feed['edgar_formtype'] == '10-K': 
	#if feed['edgar_formtype'] == '10-Q' or feed['edgar_formtype'] == '10-K': 
	
	form =  feed['edgar_formtype']
	form =  form.replace(" ","_").replace("/","-").replace(".","").replace("&","AND").replace(",","")
	print "Processing form "+str(form)
	if feed['edgar_formtype'] == '10-Q' or feed['edgar_formtype'] == '10-K' or feed['edgar_formtype'][0:3] == '8-K': 


		#file =  str(url[url.rindex("/")+1:])
		#name = feed['description']
		name = feed['edgar_companyname']
		fn_name = name.replace(" ","_").replace("/","-").replace(".","").replace("&","AND").replace(",","")
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

		loaded_path = loaded_path +file_date+"/"+fn_name+"/"+period+"/"+form+"/"
		call(["mkdir","-p",loaded_path[:-1]])

		try:
       			cursor.execute(" select aeh_sk from archive_extract_history where cik = \""+str(cik)+"\" and period = \""+str(period)+"\" and form = \""+form+"\"")
		        result = cursor.fetchone()[0]
			try:
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



		if new_file == 0:
			print "Skipping "+name+".  Already loaded!"
	
		if new_file == 1:

			print "name = "+name
			xbrl_found = 0	
			try:
				url = feed['id']
				print "url = "+url
				zip_name = loaded_path + "payload.zip"
				if  os.path.isfile(zip_name) == False:
					call(["wget", "-q", "-O", zip_name, url])
					call(["unzip","-q", "-d",loaded_path, zip_name])

				for file in sorted(glob.glob( os.path.join(loaded_path, '*[0-9].xml') )):
					if is_xbrl(file) == 1:
						xbrl_found = 1
						break
			except:
				try:
					xbrl_link = feed['edgar_xbrlfile']['url']
					xbrl_file = xbrl_link[xbrl_link.rindex("/")+1:]
					xbrl_file = loaded_path + xbrl_file	
					if  os.path.isfile(xbrl_file) == False:
						call(["wget", "-q", "-O", xbrl_file, xbrl_link])
					if is_xbrl(xbrl_file) == 1:
						xbrl_found = 1
					
				except:	
					print "New RSS Feed structure"
					for i in feed:
						print "entity = "+str(i)
						print "value = "+str(feed[i])
					sys.exit(1)

			#basename = name.replace(" ","_")+"_"+form.replace(" ","_")
			basename = fn_name+"_"+form.replace(" ","_")
			loaded_fn = loaded_path + basename
			loaded_fn = loaded_fn.replace(".xml","_"+form+".xml")
			html_base_fn = loaded_path + "html/"
			html_extension_fn = basename+".html"
			# Pull down the html 
			try:
				print "pulling link: "+link
				print "Landing to "+loaded_path
				htm_link = pull_html(form,cik,file_date,loaded_path,html_base_fn,html_extension_fn,link)

				try:
					cursor.execute("insert into archive_extract_history (`cik`,`name`,`period`,`form`,`date_id`,`path`,`xbrl`) values ('"+str(cik)+"','"+name+"','"+period+"', '"+str(form)+"', "+str(date_id)+",'"+loaded_path+"','"+str(xbrl_found)+"')")
					conn.commit()
					cursor.execute("select aeh_sk from archive_extract_history order by eh_sk desc limit 1")
					aeh_sk = cursor.fetchone()[0]

				except cursor.Error, e:
					try:   
						e.args[1].find("Duplicate")
					except:
						print "Error %d: %s" % (e.args[0],e.args[1])
						print "Failed to insert extract history value: "+str(cik)
					



				#try:

				#	fulfill_archive_html.fulfill(file_date,0,0,form,company_sk,aeh_sk)
				#except:
				#	print "no html fulfill for you! "+company_sk, name, symbol, form


			except:
				pass


			print "Done with "+name
			print
			#sys.exit(0)					


cursor.close()
conn.commit()
conn.close()


