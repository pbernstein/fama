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

        CIK = "FAILURE"
        SIC = "FAILURE"
		name = "FAILURE"

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

        source = open("temp.html")
        for line in source:
                if line.find('class="companyName"') != -1:
                       name = line.split(">")[1].split("<")[0].strip()
                       name = name.replace(" ","_").replace("/","-").replace(".","").replace("&","AND").replace(",","")
        
        source.close()


        source = open("temp.html")
        for line in source:
                if line.find("SIC=") != -1:
                        for entry in line.split("&amp;"):
                                if entry.find("SIC=") != -1:
                                        SIC = entry[entry.index("=")+1:]
        source.close()
        time.sleep(1)
        return(CIK, SIC, name)	


def load_changes(fn):
	end_dt_default = 10000000000

	f = open(fn)
	f.readline()
	exchange_list = ['AMEX','NASDAQ','NYSE']	
	defined_start_date_symbol_list = []
	for row in f:
		if row.find("NASDAQ") != -1 or row.find("NYSE") != -1 or row.find("AMEX") != -1:
			print "row = "+str(row)
			date = row.split("\t")[0]
			old_exchange = row.split("\t")[1]
			old_symbol = row.split("\t")[2]
			new_exchange = row.split("\t")[3]
			new_symbol = row.split("\t")[4].split("\r\n")[0]
			
			cursor.execute ("SELECT date_id from dates where date = \""+str(date)+"\"") 
			date_id = str(cursor.fetchone()[0])


			if not exchange_list.__contains__(old_exchange):
				# I am a newly added symbol!  Hooray for commerce!	
				new_listing = 1
			else:
				new_listing = 0

			if not exchange_list.__contains__(new_exchange):
				# I am a delisted symbol! The public can suck it!
				delisting = 1
			else:
				delisting = 0
			if delisting == 0 and new_listing == 0:
				change = 1
			else:
				change = 2
			



			if delisting == 1 or change == 1:
				old_CIK,old_SIC, name = get_cik(old_symbol)

				# insert old_symbol into table start <date -1>, end <date>	
				try:
					cursor.execute("insert into symbol (`name`,`symbol`,`exchange`,`cik`,`sic`,`start_date_id`,`end_date_id`,`current`) VALUES (\""+str(name).upper()+"\",\""+ str(old_symbol).upper()+"\",\""+ str(old_exchange).upper()+"\",\""+str(old_CIK)+"\",\""+str(old_SIC)+"\",8035,"+str(date_id)+",0)")
					conn.commit()
				except:
					pass

			if new_listing == 1 or change == 1:
				defined_start_date_symbol_list.append(new_symbol)


	if 1 == 1:
		cursor.execute("select symbol_sk, symbol from symbol where start_date_id = 8148")

		results = cursor.fetchall()
		for result in results:
				symbol_sk = result[0]
				symbol = result[1]
				if defined_start_date_symbol_list.__contains__(symbol):
					continue
				else:
					cursor.execute("update symbol set start_date_id = 8035 where symbol_sk = "+str(symbol_sk))
					conn.commit()
			


fn = sys.argv[1]

load_changes(fn)
			

cursor.close()
conn.commit()
conn.close()



