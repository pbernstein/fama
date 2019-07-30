#!/usr/bin/python

import os
import glob
from time import strptime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

# SET GLOBALS
conn = db.get_conn()
cursor = conn.cursor()


# This works because I am pulling the date out of the filename, it isn't driven bya n arugment or "today" 

def load_data(exchange):

	path = "/media/data/id/history"
	total = 0

	for file in sorted(glob.glob( os.path.join(path, exchange.upper()+'*.txt') )):

	    insert_data = ""
		date_id = ""
		cursor.execute ("SELECT date_id from dates where date = \""+str(file[file.index("_")+1:file.index(".")])+"\"") 
        date_id = cursor.fetchone()[0]
	    print "current file is: " + file
		print "date = "+str(date_id)
	    handle = open(file)
        handle.readline() # Get rid of header
        for row in handle:
		 	try:	
				percent_change = str((float(row.split(",")[5])-float(row.split(",")[2]))/float(row.split(",")[2]))
			except:
				percent_change = str(float(0.00))	
        	        try:
                        insert_data = "('"+row.split(",")[0]+"',"+str(date_id)+",'"+exchange.upper()+"',"+row.split(",")[2]+","+row.split(",")[3]+","+row.split(",")[4]+","+row.split(",")[5]+","+str(float(row.split(",")[5])-float(row.split(",")[2]))+","+percent_change+","+str(int(row.split(",")[6]))+")"
                    except:
						if row[0].isalpha():
	                        print "This row has bad data "+row
			total = total + 1
		
		
			try:
				cursor.execute ("INSERT INTO asset_value (`asset`, `date_id`, `exchange`, `open`, `high`, `low`,`close`, `change`, `percent_change`,`volume`) VALUES "+insert_data)
			except:
            	print "Cannot insert!  Probable a Foreign Key constraint."
			conn.commit()



def drop_table():
	# DROP TABLE
	try:
		cursor.execute (" drop table "+table+";")
	except:
		"Table doesn't exist yet!"


def create_table():
	# CREATE TABLE (ASSUMES DATE DIM EXISTS)
	try:
		cursor.execute (""" CREATE TABLE `asset_value` (
		  `idasset_value` int(11) NOT NULL AUTO_INCREMENT,
		  `date_id` bigint(20) DEFAULT NULL,
		  `asset` varchar(45) DEFAULT NULL,
		  `exchange` varchar(45) DEFAULT NULL,
		  `open` double DEFAULT NULL,
		  `high` double DEFAULT NULL,
		  `low` double DEFAULT NULL,
		  `close` double DEFAULT NULL,
		  `volume` int(11) DEFAULT NULL,
		  `change` double DEFAULT NULL,
		  `percent_change` double DEFAULT NULL,
		  PRIMARY KEY (`idasset_value`),
		  KEY `asset_index` (`asset`),
		  KEY `asset_date_index` (`date_id`),
		  UNIQUE KEY `uc_AssetDateID` (`asset`,`date_id`)
		) ENGINE=InnoDB AUTO_INCREMENT=15080 DEFAULT CHARSET=latin1 """)
	except:
		"Unable to create table"		




insert_data = ""
table="asset_value"



#DO NOT UNCOMMENT THIS BLOCK UNLESS YOU KNOW WHAT YOU ARE DOING!!!!
#DO_NOT_drop_table()
#DO_NOT_create_table()

# What do you want to load from scratch?
#load_data("amex")
#load_data("nyse")
load_data("nasdaq")


cursor.close()
conn.commit()
conn.close()



