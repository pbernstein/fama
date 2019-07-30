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
import feedparser
import hashlib
import MySQLdb
import shutil
import filecmp


conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()



f = open("/home/peter/work/edgar/sic_ref.csv")
for record in f:
	record = record.replace("\n","")
	sic = record[:record.find(",")]
	sic_name = record[record.find(",")+1:]
	print sic
	print sic_name


	cursor.execute("  insert into sic_ref (sic, sic_name) values ("+sic+",\""+str(sic_name)+"\")")
conn.commit()
cursor.close()
conn.close()
