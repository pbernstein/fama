#!/usr/bin/python
import MySQLdb
import os
import glob
import sys
from subprocess import call
import time
from time import strptime
import  tarfile

conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()



def get_cik(name,symbol):
	"""
	Add fuctionality:
		- apply all the mangling of the name and try to match against what i have stored in compnay, i should do this first
			- validate i am adding new companies to the company table ( pretty sure i am )
		- check more variants against the website
	"""
	org_name = name
	CIK = "FAILURE"
	SIC = "FAILURE"
	name = name + " "
	name = name.upper()
	name = name.replace('-',' ')
	name = name.replace('_',' ')
	name = name.replace('\\',' ');
	name = name.replace('/',' ');
	name = name.replace(':',' ');
	name = name.replace( '#',' ');
	name = name.replace( '&',' AND ');
	name = name.replace( ',',' ');
	name = name.replace( ' .COM ',' ');
	name = name.replace( '.',' ');
	name = name.replace( 'THE ',' ');
	name = name.replace( ' LP ',' ');
	name = name.replace( ' L P ',' ');
	name = name.replace( ' L  P ',' ');
	name = name.replace( ' LLC ',' ');
	name = name.replace( ' L L C ',' ');
	name = name.replace( ' L  L  C ',' ');
	name = name.replace( ' CO ',' ');
	name = name.replace( ' COMPANY ',' ');
	name = name.replace( ' INCORPORATED ',' ');
	name = name.replace( ' INCORPORATION ',' ');
	name = name.replace( ' INC ',' ');
	name = name.replace( ' CORPORATION ',' ');
	name = name.replace( ' CORPORA ',' ');
	name = name.replace( ' TRUST ',' ');
	name = name.replace( ' CORP ',' ');
	name = name.replace( ' CP ',' ');
	name = name.replace( ' TECHNOLOGIES ',' ');
	name = name.replace( ' TECHNOLOGY ',' ');
	name = name.replace( ' PARTNERSHIP ',' ');
	name = name.replace( ' PARTNERS ',' ');
	name = name.replace( ' INSURANCE ',' ');
	name = name.replace( ' AMERICAN ',' ');
	name = name.replace( ' AMER ',' ');
	name = name.replace( ' INTERNATIONAL ',' ');
	name = name.replace( ' INTL ',' ');
	name = name.replace( ' COMMON STOCK ',' ');
	name = name.replace( ' COMMON STOC ',' ');
	name = name.replace( ' CLASS A ',' ');
	name = name.replace( ' CLASS B ',' ');
	name = name.replace( ' CLASS C ',' ');
	name = name.replace( ' PREFERRED ',' ');
	name = name.replace( ' PFD ',' ');
	name = name.replace( ' PF ',' ');
	name = name.replace( ' SERIES A ',' ');
	name = name.replace( ' SERIES B ',' ');
	name = name.replace( ' SERIES C ',' ');
	name = name.replace( ' CON ',' ');

		  

        name = name.replace(" ","_")
        name = name.rstrip("_")
        name = name.lstrip("_")



	if (
	name.strip() == "" or 
	symbol.find(".") != -1 or 
	name.find(" ETF") != -1 or
	name.find(" ETN") != -1 or
	name.find(" SECTOR") != -1 or
	name.find(" BOND ") != -1 or
	name.find(" BOND") != -1 or
	name.find(" DIVIDEND ") != -1 or
	name.find(" DIVIDEND") != -1 or
	name.find(" TRUST") != -1 or
	name.find(" HEDGE") != -1 or
	name.find(" ISHARES") != -1 or
	name.find(" QUANTSHARES") != -1 or
	name.find(" SHARES") != -1 or
	name.find("MSCI ") != -1 or
	name.find(" FUND") != -1 or
	name.find(" WISDOMTREE") != -1 or
	name[0:2] == "S&"
	):
		return(CIK, SIC)



	print "querying sec name = "+name+"| org name = "+org_name


	"""
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
	"""





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

	# Try Fuzzy Hit	
	if CIK == "FAILURE":
		source = open("temp.html")
		
		fuzzy_hit = 0 
		for line in source:
			#print line
			if line.upper().find('Companies with names matching'.upper()) != -1:
				#print "found a fuzzy hit"
				fuzzy_hit = 1
		source.close()

		if fuzzy_hit == 1:
			lf = open("temp.dump","w")
			call(["lynx", "-dump", "temp.html"], stdout=lf)
			lf.close()

			source = open("temp.dump")
			prev = ""
			for line in source:
				if prev == "":
					prev = line	
					continue
				if line.find('SIC') != -1:
					prev = prev.split(" ")[3]
					CIK = prev[prev.index("]")+1:]
					line = line.split(" ")[4]
					SIC = line[line.index("]")+1:]
		source.close()


	# Try modified name
	if CIK == "FAILURE" and name.find("_INC") != -1:
		#name = name[:name.index("_INC")]
		name = name.replace("_INC","%20inc")
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

	#if CIK == "FAILURE":
		#"""
		#try to match the name from eod to the company table
		#	if it hits, take the CIK!
		#am i even updating the company table?
#
#		"""

	source = open("temp.html")
	for line in source:
		if line.find("SIC=") != -1: 
			for entry in line.split("&amp;"):
				if entry.find("SIC=") != -1: 
					SIC = entry[entry.index("=")+1:]
	source.close()
        #source = open("temp.html")
        #for line in source:
        #        if line.find('class="companyName"') != -1:
        #                name = line.split(">")[1].split("<")[0].strip()
	#		name = name.replace(" ","_").replace("/","-").replace(".","").replace("&","AND").replace(",","")
	#
        #source.close()

	time.sleep(1)
	#print "found cik = "+CIK+" for name |"+name+"| and symbol |"+symbol	]
	if CIK != 'FAILURE':
		print " CIK = "+CIK
	return(CIK, SIC)


	"""			
	"""			


if __name__ == '__main__':
        name = sys.argv[1]
	print "name: "+name
        cik = get_cik(name,"")
        print "cik is: "+str(cik)




cursor.close()
conn.commit()
conn.close()



