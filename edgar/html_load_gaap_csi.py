#!/usr/bin/python
# html_load.py 


import sys
import re
import glob
import os
import shutil
import MySQLdb
from time import strptime
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from operator import itemgetter, methodcaller
import date_parse
import table_reader
import find_candidate



def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def remove_dupes(seq):
   # not order preserving
   set = {}
   map(set.__setitem__, seq, [])
   return set.keys()


def file_get_contents(filename):
    with open(filename) as f:
        return f.read()


#failed html_load_gaap.html_load(AMERISOURCEBERGEN CORP, 0001140859, 2013-07-16, 8-K, ABC, 15636

def html_load(company, cik, file_date, form, symbol,eh_sk, html_fn = ""):
	#print "in html_load"
	print "in load: "+html_fn
	conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
	cursor = conn.cursor ()

	html_path = "/media/data/investments/data/edgar/forms/rss/loaded/html/"+file_date+"/"+str(cik)
	print  " select date_id from dates where date = \""+str(file_date)+"\""
	cursor.execute(" select date_id from dates where date = \""+str(file_date)+"\"")
	row = cursor.fetchone()
	file_date_id = row[0]


	#print "looking here for a table "+html_path
	#print glob.glob( os.path.join(html_path, '*.html'))
	inserts = 0
	print html_path
	file = html_fn
	#for file in sorted(glob.glob( os.path.join(html_path, '*.html') )):
	if 1 == 1:
		print "looking here for a table "+str(file)
		new_dates = []

		count = 0
		count = count + 1
	
		print "Loading "+file
	
		#print "attempting to do the table read  "
		try:
			data = table_reader.main(file)
		except:
			print "failed finding table"

		try:
			#print "printing data in html_load"
			if data == []:
				print "emptry set"
				#continue	
			#for row in data:
			#	print row
		except:
			print "can't print data, bailing!"
			#continue

		# ['Accounts receivable, less allowances of $75 and $58, respectively', '2,820', '2012-12-31']
		# ['Accounts receivable, less allowances of $75 and $58, respectively', '2,132', '2012-03-31']
	
		f = open(file)	
		result = ""
		attributes = []
		company = "\""+company+"\""
		cik = "\""+cik+"\""

		try:

			candidate, candidate_period, period_quarter_map = find_candidate.get_candidate(file_date_id, form, data, "html")
		except:
			print "failed in find_candidate"
		#print "post find candidate"


		try:
			if candidate == "RETURN 1":
				return 1
			if candidate == "INVALID FORMAT":
				return 1
			if candidate == "FAIL":
				return 1
		except:
			return 1 

		#print "candidate period = "+str(candidate_period)
		cursor.execute(" select date_id from dates where date = \""+str(candidate)+"\"")
		row = cursor.fetchone()
		date_id = row[0]

		name = ""
		cursor.execute(" select name from company where cik = "+str(cik))
		row = cursor.fetchone()

		try:
			name = row[0]

			if name != None and name != company.replace("\"",""):
				print "10q and DB have a CIK/company name mismatch!!!"
				print "10Q:"+ name
				print "DB:"+ company
		except:
			try:
				print "inserting company information: "
				print "insert into company (`name`, `cik`, `industry`, `industry_id`, `corp_state`, `address_line_1`, `address_line_2`, `city`, `state`, `zip`) values ("+",".join(map(str,[company, cik, industry, industry_id, corp_state, address_line_1, address_line_2, city, state, zip]))+")"
				cursor.execute ("insert into company (`name`, `cik`, `industry`, `industry_id`, `corp_state`, `address_line_1`, `address_line_2`, `city`, `state`, `zip`) values ("+",".join(map(str,[company, cik, '', '', '', '', '', '', '', '']))+")")
				conn.commit()
			except cursor.Error, e:
				try:
					e.args[1].find("Duplicate")
				except:
					print "Error %d: %s" % (e.args[0],e.args[1])
					print "failed to insert company info: "+",".join(map(str,[company, cik, industry, industry_id, corp_state, address_line_1, address_line_2, city, state, zip]))
				#shutil.move(file,error_canada_path+"/"+file[file.rindex("/")+1:].replace(".","__"+str(datetime.now()).replace(" ","_")+"."))
					#continue
			
		

		cursor.execute(" select company_sk from company where cik = "+str(cik))
		row = cursor.fetchone()
		company_sk = row[0]



		for a in data:
			# example 
			# a = [' Cash and cash equivalents', '93935000', '2012-11-24']
			# or
			# a = [' Foreign currency translation adjustment, net of tax', '291000', '2012-08-24|;|2012-11-24']
			#if a[2].find("2011") == -1:
			#	print "a = "+str(a[2])
			try:
				#if candidate_period[a[2]] == candidate or candidate_period[a[2].replace("-","")] == candidate:
				if candidate_period[a[2]] == candidate:
					new_info = 1
				else:
					new_info = 0
			except:
					new_info = 0
			inserts = inserts + 1
			try:
					#value = a["value"].replace("\"","")
					value = a[1]
					if value.find(",") != -1 or value.find("$") != -1 or value.find(")") != -1:
						value = value.replace(",","")
						value = value.replace("$","")
						value = value.replace(")","")
					value = "\""+str(value)+"\""

					try:
						validation = re.search("[a-zA-Z]",value).pos
						print "Trying to assign value of "+value+" to "+attribute+".  Bailing!"
						continue
					except:
						pass
			except:
					pass
		
			attribute = a[0]
			if attribute[0] == " " or attribute[len(attribute)-1] == " ":
				attribute = attribute.lstrip().rstrip()

			try:

						cursor.execute("select * from gaap_value where company_sk = "+str(company_sk)+" and date_value = \""+a[2]+"\" and attribute = \""+attribute+"\" and source = 'h' limit 1")
						result = cursor.fetchone()

						if result == None:
							cursor.execute("insert into gaap_value (`company_sk`, `attribute`, `unit`, `value`, `date_id`, `file_date_id`,`date_value`,`period`,`source`,`new_info`,`eh_sk`) values ("+",".join(map(str,[company_sk,  "\""+attribute+"\"", "\"usd\"", value , date_id, file_date_id, "\""+a[2]+"\"", "\""+period_quarter_map+"\"","\"h\"",new_info,eh_sk]))+")")
							conn.commit()	
						else:
							print str(result)
							pass
			except cursor.Error, e:
						try:
							e.args[1].find("Duplicate")
							print "In gaap_value insert Error %d: %s" % (e.args[0],e.args[1])
							#print str(a)
			
						except:
							print "Error %d: %s" % (e.args[0],e.args[1])
							print "Failed to insert gaap value: "+str(a)
							
	 
		conn.commit()	

	cursor.close()
	conn.close()
	#print "completed html_load loop"
		
	if inserts < 10:
		print "Only Inserted "+str(inserts)+" rows"
		print "Invalid dates:"
		unique_new_dates = remove_dupes(new_dates)
		for nd in unique_new_dates:
			if nd != "IGNORE ME":
				print nd +" | "+ str(context_counts[nd])
		return 1
	else:
		return 0 #period_quarter_map[candidate]
		




if __name__ == '__main__':
        company = sys.argv[1]
        cik = sys.argv[2]
        file_date = sys.argv[3]
        form = sys.argv[4]
        symbol = sys.argv[5]
        eh_sk = sys.argv[6]
        html_fn = sys.argv[7]
	print company
	print cik
	print file_date	
        html_load(company, cik, file_date,form,symbol,eh_sk, html_fn)
		
