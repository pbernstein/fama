#!/usr/bin/python

import os
import glob
import sys
from subprocess import call
import time
from time import strptime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

# SET GLOBALS
conn = db.get_conn()
cursor = conn.cursor()


def get_cik(symbol):
	# Find the CIK	/ NAME
	base_link = "http://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK=[SYMBOL]&filenum=&State=&Country=&SIC=&owner=exclude&Find=Find+Companies&action=getcompany"
	link = base_link.replace("[SYMBOL]",symbol)	
	call(["wget", "-q", "-O", "temp.html", link])	
	source = open("temp.html")
	CIK = "FAILURE"
	SIC = "FAILURE"
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

def load_changes():
	path = "/media/data/investments/data/assets/names/"
	print "Loading new changes"
	try:
		file = path+"Changes.txt"
		handle = open(file)
        handle.readline() # Get rid of header
        for row in handle:
			update_date = row.split("\t")[0]
			old_exchange = row.split("\t")[1]
			old_symbol = row.split("\t")[2]
			new_exchange = row.split("\t")[3]
			new_symbol = row.split("\t")[4]



			if old_exchange.find("AMEX") != -1  or old_exchange.find("NYSE") != -1 or old_exchange.find("NASDAQ") != -1:
				pass

					
			elif new_exchange.find("AMEX") != -1  or new_exchange.find("NYSE") != -1 or new_exchange.find("NASDAQ") != -1:
				pass

	except:
		print "died in changes"
		


def load_names(exchange,date):
	end_id_default = 10000000000	
	# Read all the scrape_* files in this folder
	path = "/media/data/investments/data/assets/names/"
	print exchange.upper()+".txt"
	total = 0
	for file in sorted(glob.glob( os.path.join(path, '*') )):
	     if exchange.upper()+".txt" == file.split("/").pop(): 
	        insert_data = ""
		date_id = ""
		cursor.execute ("SELECT date_id from dates where date = \""+str(date)+"\"") 
        date_id = cursor.fetchone()[0]
	    print "current file is: " + file
		print "date = "+str(date_id)
	    handle = open(file)
        handle.readline() # Get rid of header
					
        for row in handle:


			symbol = row.split("\t")[0]
			new_name = row.split("\t")[1].split("\r\n")[0]
			new_name = new_name.upper()
			exchange = exchange.upper()

			# Do I already exist in the table?
			cursor.execute("select name, cik from symbol where symbol = \""+symbol+"\" and exchange = \""+exchange+"\" and end_date_id = "+end_id_default)
			result = cursor.fetchone()
			if result == None:
				stored_name = None
			else:
				stored_name = result[0]
				stored_cik = result[1]

			if stored_name == None:
				# Entirely new row!  Weeee!
				CIK,SIC = get_cik(symbol)
				# insert everything into symbol with end_date_id = NULL 
				

				print "insert into symbol (`name`,`symbol`,`exchange`,`cik`,`sic`,`start_date_id`) VALUES (\""+new_name+"\",\""+ str(symbol).upper()+"\",\""+ str(exchange).upper()+"\",\""+CIK+"\",\""+SIC+"\","+str(date_id)+")"
				try:
					cursor.execute("insert into symbol (`name`,`symbol`,`exchange`,`cik`,`sic`,`start_date_id`,`current`) VALUES (\""+str(new_name).upper()+"\",\""+ str(symbol).upper()+"\",\""+ str(exchange).upper()+"\",\""+CIK+"\",\""+SIC+"\","+str(date_id)+",1)")
				except:
					print "failed to insert"

				conn.commit()

				continue

			if stored_name != new_name:
				# Is this symbol is talking about a different company?
				CIK,SIC = get_cik(symbol)
				if CIK != stored_cik:
						
					cursor.execute("update symbol set end_date_id = "+str(date_id)+" where cik = \""+stored_cik+"\" and end_date_id = "+end_id_default)
					cursor.execute("update symbol set current = 0 where cik = \""+stored_cik+"\" and current = 1")
					cursor.execute("insert into symbol (`name`,`symbol`,`exchange`,`cik`,`sic`,`start_date_id`,`current`) VALUES (\""+str(new_name).upper()+"\",\""+ str(symbol).upper()+"\",\""+ str(exchange).upper()+"\",\""+CIK+"\",\""+SIC+"\","+str(date_id)+",1)")
				else:
					# update name in the symbol table to new_name
					print "update symbol set name = \""+str(new_name).upper()+"\" where cik = \""+stored_cik+"\" and end_date_id = "+end_id_default
					cursor.execute("update symbol set name = \""+str(new_name).upper()+"\" where cik = \""+stored_cik+"\" and end_date_id = "+end_id_default)

				sys.exit(0)


			else:
			# else, stored name = new name, so carry on..  ( leave end_date_id of existing record as NULL ) 
				print "nothing to see here.. "
					
				

			

				
		
try:
	date = sys.argv[1]
except:
	print "Pass me the date fool!"
	sys.exit(0)

insert_data = ""



load_names("amex",date)
load_names("nyse",date)
load_names("nasdaq",date)



cursor.close()
conn.commit()
conn.close()



