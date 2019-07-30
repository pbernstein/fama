#!/usr/bin/python

import os
import glob


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

# SET GLOBALS
conn = db.get_conn()
cursor = conn.cursor()

insert_data = ""
table="fama"


# DROP TABLE
try:
	cursor.execute (" drop table "+table+";")
except:
	print "Table doesn't exist yet"


# CREATE TABLE (ASSUMES DATE DIM EXISTS)

cursor.execute (""" CREATE TABLE `fama` (
  `idfama` int(11) NOT NULL AUTO_INCREMENT,
  `mrkt_rf` double DEFAULT NULL,
  `smb` double DEFAULT NULL,
  `hml` double DEFAULT NULL,
  `rf` double DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`idfama`),
  FOREIGN KEY (`date_id`) REFERENCES dates(`date_id`) 
) ENGINE=InnoDB AUTO_INCREMENT=15080 DEFAULT CHARSET=latin1 """)


# POPULATE

# Read all the scrape_* files in this folder
path = "/home/peter/data/fama/" 
insert_data = ""
handle = open(path+"F-F_Research_Data_Factors_daily.load")
for row in handle:
	if (row.split(",")[0] != "Date" and row.find("NA") < 0):
		unparsed_date = row.split(",")[0]
		parsed_date = unparsed_date[:4]+"-"+unparsed_date[4:6]+"-"+unparsed_date[6:]
		cursor.execute( """ select date_id from dates where date = %s""",parsed_date )
		result = cursor.fetchone()
		if (result != None):
			date_sk = result[0]
			insert_data = insert_data +"("+str(date_sk)+","+row.split(",")[1]+","+row.split(",")[2]+","+row.split(",")[3]+","+str(float(row.split(",")[4]))+"),"
	
insert_data = insert_data[:-1]

#print "insert data = "+insert_data
cursor.execute ("INSERT INTO "+table+" (`date_id`, `mrkt_rf`, `smb`, `hml`, `rf`) VALUES "+insert_data)

cursor.close()
conn.commit()
conn.close()


