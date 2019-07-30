#
# Usage:

import re
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
import utility


conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()







file_date = sys.argv[1]
year = file_date.split("-")[0]
date = file_date.replace("-","")

temp_path = "/master/history/staging/forms/"+year+"/"
#temp_path = "/media/data/investments/data/edgar/forms/eod/forms/"+year+"/"
bkp_path = "/media/data/investments/data/edgar/forms/eod/form_bkp/"+year+"/"
#bkp_path = "/master/history/staging/"+year+"/"


cursor.execute(" select date_id from dates where date = \""+str(date)+"\"")
row = cursor.fetchone()
date_id = row[0]


call(["rm", "-rf", temp_path])
call(["mkdir", "-p", temp_path])
csi_handle = open("/home/peter/work/edgar/chTicker_csi_all_pipes_with_8k")
csi_out = open("/home/peter/work/edgar/chTicker_csi_unique_"+year,"a")

key_cik = ""
key_date_id = ""
key_url  = ""

for idx_record in csi_handle:


        idx = idx_record.split("|")
        cik = idx[2]
        cik = cik.zfill(10)
        url = idx[5]
        form = idx[3]
        #date_id = idx[4]
	filing_date_id = idx[4]

        if cik == key_cik and filing_date_id == key_date_id  and url == key_url:
                continue
        else:
                key_cik = cik
                key_date_id  = filing_date_id
                key_url  = url

        exchange = idx[8].replace("\n","")
        symbol = idx[7]
        name = idx[1]
        #print url
	if (str(filing_date_id) == str(date_id)) and (form ==  '10-Q' or form == '10-K' or form == '8-K'):


			call(['/home/peter/work/edgar/get_period.ksh','ftp://ftp.sec.gov/'+url,'/tmp/period'])
			period_handle = open('/tmp/period')
			for row in period_handle:
				period = row.split("\n")[0]
        		csi_out.write(cik+"|"+form+"|"+ filing_date_id+"|"+ symbol+"|"+ exchange+"|"+ period+"|"+ url+"|"+name+"\n")

			txt_url = "ftp://ftp.sec.gov/"+idx[5].replace("\n",'')
			basename = exchange+"_"+symbol+"_"+file_date+"_"+form+"_"+period
			txt_name = temp_path+basename+".txt"
			print txt_name

			call(["wget", "-q", "-O", txt_name, txt_url])
		


csi_handle.close()
csi_out.close()

call(["rm", "-f", bkp_path+"eod_"+date+".tar.gz"])
call(["tar", "-czf", bkp_path+"eod_"+date+".tar.gz", temp_path])
print "Archiving downloaded forms:", bkp_path+"eod_"+date+".tar.gz"

call(["rm", "-rf", temp_path])
#call(["gzip","-f", idx_name])


cursor.close()
conn.commit()
conn.close()



