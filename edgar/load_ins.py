#!/usr/bin/python

import MySQLdb
import buckets

conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()
columns =  buckets.columns
count = 1
for i in columns:
		cursor.execute("insert into iset (`i_attribute`, `priority`) values ("+",".join(map(str,["\""+i+"\"", count]))+")")
		count = count + 1
			

conn.commit()
cursor.close()
conn.close()

