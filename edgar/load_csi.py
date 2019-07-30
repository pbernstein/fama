#!/usr/bin/python

#
# Usage:

import sys
import os
import MySQLdb


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
for idx_record in csi_handle:
	idx = idx_record.split("|")
	cik = idx[2]
        cik = cik.zfill(10)
	exchange = idx[8].replace("\n","")
	symbol = idx[7]
	date_id = idx[4]
	name = idx[1]
	
	#print " insert into csi_symbols (symbol, exchange, cik, date_id, name) values ('"+symbol+"','"+exchange+"','"+cik+"','"+date_id+"','"+name+"')"
	#sys.exit(0)
	cursor.execute(" insert into csi_symbols (symbol, exchange, cik, date_id, name) values ('"+symbol+"','"+exchange+"','"+cik+"','"+date_id+"','"+name+"')")


cursor.close()
conn.commit()
conn.close()				

