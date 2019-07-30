#!/usr/bin/python

import os
import glob
import sys
from subprocess import call
import time
from time import strptime
import  tarfile
from get_cik import get_cik
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

# SET GLOBALS
conn = db.get_conn()
cursor = conn.cursor()


def retry_failed_lookups(exchange):
		cursor.execute('select symbol_sk, name,symbol from symbol where cik = "FAILURE" and exchange = "'+exchange.upper()+'"')
		results = cursor.fetchall()
		for result in results:
				sk = str(result[0])
				name = str(result[1])
				symbol = str(result[2])
				CIK, SIC = get_cik(name,symbol)	
				if CIK == "FAILURE":
					#print "Still no luck with "+sk, name
					pass
				else:
					#print "Found "+name, CIK, SIC
					cursor.execute('update symbol set CIK = "'+CIK+'", SIC = "'+SIC+'" where symbol_sk = '+sk)
					conn.commit()
				
					
	


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
#			print i.split("\t")[0], i.split("\t")[1].split("\n")[0]
			

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
			#if symbol == 'SSTK':
			#	print "found shutterstock 2"
			#	print stored_handle_data.pop()
			#	sys.exit(0)





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
		

		

		#Second Pass	  	
		# take all name/symbol/exchange combinations and validate they exist in the table.  If it doesn't, lookup the cik/sic and insert using start_date_id = today and default end date
		#stored_handle_data.append([symbol,eod_name,name_cik_request,exchange])
		for row in  stored_handle_data:
			symbol = row[0]
			eod_name = row[1]
			name_cik_request = row[2]
			exchange = row[3]

			# Do I already exist in the table?
			cursor.execute("select cik, symbol_sk from symbol where name = \""+eod_name+"\" and symbol = \""+symbol+"\" and exchange = \""+exchange+"\" and current = 1")
			results = cursor.fetchall()
			found = 0
			update = 0
			symbol_sk = 0
			for result in results:
				if result[0] != None and result != 'FAILURE':
					found = 1
				if result[0] == 'FAILURE':
					update = 1
					symbol_sk = result[1]

			if found == 0:				
				CIK,SIC = get_cik(name_cik_request,symbol)
				
				try:
					cursor.execute("insert into symbol (`name`,`symbol`,`exchange`,`cik`,`sic`,`start_date_id`,`end_date_id`,`current`) VALUES (\""+str(eod_name).upper()+"\",\""+ str(symbol).upper()+"\",\""+ str(exchange).upper()+"\",\""+CIK+"\",\""+SIC+"\","+str(date_id)+","+end_date_id_default+",1)")
				except:
					print "failed to insert"
					print "insert into symbol (`name`,`symbol`,`exchange`,`cik`,`sic`,`start_date_id`,`end_date_id`,`current`) VALUES (\""+str(eod_name).upper()+"\",\""+ str(symbol).upper()+"\",\""+ str(exchange).upper()+"\",\""+CIK+"\",\""+SIC+"\","+str(date_id)+","+end_date_id_default+",1)"
				conn.commit()

			if update == 1:				
				CIK,SIC = get_cik(name_cik_request,symbol)

				if CIK != 'FAILURE':
						try:
							cursor.execute("update symbol set cik = \""+CIK+"\" where symbol_sk = "+str(symbol_sk))
						except:
							print "failed to update"
							print "update symbol set cik = \""+CIK+"\" where symbol_sk = "+str(symbol_sk)
							sys.exit(0)

				conn.commit()



def load_compressed_files(date):
	path = "/media/data/investments/data/assets/compressed_scrape"
	exchange_dict = {}

        for file in sorted(glob.glob( os.path.join(path, '*ames_'+date+'*') )):
		print "file "+file
		date = file[file.rindex("/")+1:].split("_")[1].split(".")[0].replace("-","")
		tar = tarfile.open(file,mode='r:gz')
		for member in tar.getmembers():
			name = member.name

	
			if name.find("AMEX") != -1 or name.find("NASDAQ") != -1 or name.find("NYSE") != -1:
#			if name.find("NYSE") != -1:
				
				if name.find("AMEX") != -1:
					exchange = "AMEX"
				if name.find("NASDAQ") != -1:
					exchange = "NASDAQ"
				if name.find("NYSE") != -1:
					exchange = "NYSE"
				f=tar.extractfile(member)
				#data = get_file_contents(handle, date,exchange):
				#exchange_dict[exchange] = data

				
				load_symbols(f,date,exchange)
					
			
		tar.close()




date = sys.argv[1]
load_compressed_files(date)


cursor.close()
conn.commit()
conn.close()


