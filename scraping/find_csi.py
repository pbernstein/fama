#!/usr/bin/python

import os
import glob
import sys
from subprocess import call
import time
from time import strptime
import  tarfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

def get_cik(name,symbol):

	CIK = "FAILURE"
	SIC = "FAILURE"

	# Try Symbol
	base_link = "http://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK=[SYMBOL]&filenum=&State=&Country=&SIC=&owner=exclude&Find=Find+Companies&action=getcompany"
	link = base_link.replace("[SYMBOL]",symbol)	
	call(["wget", "-q", "-O", "temp.html", link])	
	source = open("temp.html")
	for line in source:
		if line.find("CIK=") != -1: 
			for entry in line.split("&amp;"):
				if entry.find("CIK=") != -1: 
					CIK = entry[entry.index("=")+1:]
	source.close()

	# Try name
	# Find the CIK	/ NAME
	if CIK == "FAILURE":
		base_link = "http://www.sec.gov/cgi-bin/browse-edgar?company=[COMPANY_NAME]&CIK=&filenum=&State=&Country=&SIC=&owner=exclude&Find=Find+Companies&action=getcompany"
		name = name.replace(" ","%20")
		name = name.replace(",","%27")
		link = base_link.replace("[COMPANY_NAME]",name)    
		call(["wget", "-q", "-O", "temp.html", link])	
		source = open("temp.html")
		for line in source:
			if line.find("CIK=") != -1: 
				for entry in line.split("&amp;"):
					if entry.find("CIK=") != -1: 
						CIK = entry[entry.index("=")+1:]
		source.close()

	# Try modified name
	if CIK == "FAILURE" and name.find("_INC") != -1:
		name = name[:name.index("_INC")]
		base_link = "http://www.sec.gov/cgi-bin/browse-edgar?company=[COMPANY_NAME]&CIK=&filenum=&State=&Country=&SIC=&owner=exclude&Find=Find+Companies&action=getcompany"
		link = base_link.replace("[COMPANY_NAME]",name)    
		call(["wget", "-q", "-O", "temp.html", link])	
		source = open("temp.html")
		for line in source:
			if line.find("CIK=") != -1: 
				for entry in line.split("&amp;"):
					if entry.find("CIK=") != -1: 
						CIK = entry[entry.index("=")+1:]
		source.close()

	source = open("temp.html")
	for line in source:
		if line.find("SIC=") != -1: 
			for entry in line.split("&amp;"):
				if entry.find("SIC=") != -1: 
					SIC = entry[entry.index("=")+1:]
	source.close()


	time.sleep(1)
	return(CIK, SIC)



def load_symbols(handle, date,exchange):
		end_date_id_default = str(10000000000)
	        insert_data = ""
		date_id = ""
		print "date = "+date+" Exchange = "+exchange
		cursor.execute ("SELECT date_id from dates where date = \""+str(date)+"\"") 
                date_id = str(cursor.fetchone()[0])
		




		# Process
		# First Pass goes through EOD files
			# take all name/symbol/exchange combinations and validate they exist in the table.  If it doesn't, lookup the cik/sic and insert using start_date_id = today and default end date

		# Second pass goes through 
			# look for all name/symbol/exchange combinations and validate they are in the file. If they are not, close the row by updating with end_date_id = today - 1

		###########################	

	
		#	 Load the file into a list
                handle.readline() # Get rid of header
		stored_handle_data = []
                for row in handle:

			

			symbol = row.split("\t")[0]
			eod_name = row.split("\t")[1].split("\r\n")[0]
			name_cik_request = eod_name.upper()
			eod_name = eod_name.upper().replace(" ","_").replace("/","-").replace(".","").replace("&","AND").replace(",","").replace("\"","'")
			exchange = exchange.upper()

			if name_cik_request.strip() == "":
				continue
			if symbol.find(".") != -1: 
				continue
			if name_cik_request.find(" ETF") != -1: 
				continue
			if name_cik_request.find(" ETN") != -1: 
				continue
			if name_cik_request.find(" SECTOR") != -1: 
				continue
			if name_cik_request.find(" BOND ") != -1: 
				continue
			if name_cik_request.find(" BOND") != -1: 
				continue
			if name_cik_request.find(" DIVIDEND ") != -1: 
				continue
			if name_cik_request.find(" DIVIDEND") != -1: 
				continue
			if name_cik_request.find(" TRUST") != -1: 
				continue
			if name_cik_request.find(" HEDGE") != -1: 
				continue
			if name_cik_request.find(" ISHARES") != -1: 
				continue
			if name_cik_request.find(" QUANTSHARES") != -1: 
				continue
			if name_cik_request.find(" SHARES") != -1: 
				continue
			if name_cik_request.find("MSCI ") != -1: 
				continue
			if name_cik_request.find(" FUND") != -1: 
				continue
			if name_cik_request.find(" WISDOMTREE") != -1: 
				continue
			if name_cik_request[0:2] == "S&": 
				continue

			stored_handle_data.append([symbol,eod_name,name_cik_request,exchange])





		# First Pass goes through EOD files
		# look for all name/symbol/exchange combinations and validate they are in the file. If they are not, close the row by updating with end_date_id = today - 1

		#cursor.execute("select symbol_sk, name, symbol from symbol where exchange = \""+exchange+"\" and start_date_id <= "+date_id+" and end_date_id > "+date_id)
		cursor.execute("select symbol_sk, name, symbol from symbol where exchange = \""+exchange+"\" and current = 1")
		results = cursor.fetchall()
		for result in results:
			symbol_sk = str(result[0])
			eod_name = str(result[1])
			symbol = str(result[2])
	
			found = 0
			for row in  stored_handle_data:
				if row[0] == symbol and row[1] == eod_name:   # exchange has to match, because we only extracted the exchange that we loaded to the file
					found = 1

			if found == 0:
				# I don't exist in the eod file anymore, close this record off
				cursor.execute("update symbol set end_date_id = "+str(int(date_id) - 1)+" where symbol_sk = "+str(symbol_sk))
				cursor.execute("select max(current) from symbol where symbol = \""+symbol+"\" and exchange = \""+exchange+"\"")
				max_current = cursor.fetchone()[0]+1
				cursor.execute("update symbol set current = "+str(max_current)+" where symbol_sk = "+str(symbol_sk))
				#print "updated "+symbol, eod_name
				conn.commit()
			#sys.exit(0)

		

		#Second Pass	  	
		# take all name/symbol/exchange combinations and validate they exist in the table.  If it doesn't, lookup the cik/sic and insert using start_date_id = today and default end date
		#stored_handle_data.append([symbol,eod_name,name_cik_request,exchange])
		for row in  stored_handle_data:
			symbol = row[0]
			eod_name = row[1]
			name_cik_request = row[2]
			exchange = row[3]

			# Do I already exist in the table?
			cursor.execute("select name from symbol where name = \""+eod_name+"\" and symbol = \""+symbol+"\" and exchange = \""+exchange+"\" and current = 1")
			results = cursor.fetchall()
			found = 0
			for result in results:
				if result[0] != None:
					found = 1

			if found == 0:				
				#print "found new row!"
				CIK,SIC = get_cik(name_cik_request,symbol)


				try:
					cursor.execute("insert into symbol (`name`,`symbol`,`exchange`,`cik`,`sic`,`start_date_id`,`end_date_id`,`current`) VALUES (\""+str(eod_name).upper()+"\",\""+ str(symbol).upper()+"\",\""+ str(exchange).upper()+"\",\""+CIK+"\",\""+SIC+"\","+str(date_id)+","+end_date_id_default+",1)")
				except:
					print "failed to insert"
					print "insert into symbol (`name`,`symbol`,`exchange`,`cik`,`sic`,`start_date_id`,`end_date_id`,`current`) VALUES (\""+str(eod_name).upper()+"\",\""+ str(symbol).upper()+"\",\""+ str(exchange).upper()+"\",\""+CIK+"\",\""+SIC+"\","+str(date_id)+","+end_date_id_default+",1)"

				conn.commit()
				#sys.exit(0)




def find_csi():
	f = open('/home/peter/work/scraping/unused_filtered.csv')
	o = open('/home/peter/work/scraping/matched_unused.csv','w')
	for record in f:
		fields = record.split(",")
		sk = fields[0]
		ticker = fields[1]
		name = fields[2]
		exchange = fields[3]
		cleanname = fields[4].replace("\n","")
		CIK,SIC = get_cik(cleanname,ticker)
		o.write(",".join([sk,ticker,name,exchange,cleanname,CIK])+"\n")

		#break
		
	f.close()
	o.close()

conn = db.get_conn()
cursor = conn.cursor()


find_csi()


cursor.close()
conn.commit()
conn.close()



