#!/usr/bin/python

#
# Usage:

import sys
import os
import MySQLdb
from subprocess import call


conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()


"""
csi_symbols | CREATE TABLE `csi_symbols` (
  `csi_sk` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(10) NOT NULL,
  `exchange` varchar(10) NOT NULL,
  `cik` varchar(20) DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
"""


csi_handle = open("/media/data/id/hpcc/chTicker_csi_all_pipes_with_8k")
csi_out = open("/media/data/id/hpcc/chTicker_unique",'w')


key_cik = ""
key_date_id = ""
key_url  = ""
stored_symbol = ""
stored_exchange = ""


new = 1
for idx_record in csi_handle:
	idx = idx_record.split("|")
	cik = idx[2]
        cik = cik.zfill(10)
	url = idx[5]
	date_id = idx[4]
	
	if cik == key_cik and date_id == key_date_id  and url == key_url:
		continue
	else:
		key_cik = cik
		key_date_id  = date_id
		key_url  = url

	exchange = idx[8].replace("\n","")
	symbol = idx[7]
	name = idx[1]
	#print url
	call(['/home/peter/work/edgar/get_period.ksh','ftp://ftp.sec.gov/'+url,'/tmp/period'])
	period_handle = open('/tmp/period')
	for row in period_handle:
		period = row.split("\n")[0]

	csi_out.write(cik+"|"+ date_id+"|"+ symbol+"|"+ exchange+"|"+ period+"|"+ url+"|"+name+"\n")
	new = new + 1
	#if new == 5:
	#	csi_out.close()
	#	csi_handle.close()
	#	sys.exit(0)
	
	
	
	#print " insert into csi_symbols (symbol, exchange, cik, date_id, name) values ('"+symbol+"','"+exchange+"','"+cik+"','"+date_id+"','"+name+"')"
	#sys.exit(0)
	#cursor.execute(" insert into csi_symbols (symbol, exchange, cik, date_id, name) values ('"+symbol+"','"+exchange+"','"+cik+"','"+date_id+"','"+name+"')")

csi_out.close()
csi_handle.close()

cursor.close()
conn.commit()
conn.close()				

