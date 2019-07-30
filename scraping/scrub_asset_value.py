#!/usr/bin/python

import os
import sys
import glob
from time import strptime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

# SET GLOBALS
conn = db.get_conn()
cursor = conn.cursor()

errors = []

date = sys.argv[1]

cursor.execute(" select date_id from dates where date = "+str(date))
row = cursor.fetchone()
date_id = row[0]

cursor.execute(" select date_id from asset_value where date_id = "+str(date_id)+" group by date_id" )

rows = cursor.fetchall()
err = open('/media/data/investments/data/scrub/asset_value_scrub_errors.sql','w')
nomatch = open('/media/data/investments/data/scrub/asset_value_scrub_nomatch.sql','w')
for row in rows:
	date_id = int(row[0])
	cursor.execute(" select date from dates where date_id = "+str(date_id) )
	row = cursor.fetchone()
	date = row[0]
	print "running "+str(date)
	f = open('/media/data/investments/data/scrub/asset_value_scrub_'+str(date_id)+'.sql','w')
	yahoo_asset = ""
	yahoo_open = 0
	yahoo_close = 0
	yahoo_volume = 0
	google_asset = ""
	google_open = 0
	google_close = 0
	google_volume = 0

	cursor.execute( " select asset, round(open,2), round(close,2), volume from asset_value where date_id = " +str(date_id))
	results = cursor.fetchall()

	for result in results:
		asset = result[0]
		eod_open = result[1]
		eod_close = result[2]
		eod_volume = result[3]
		yahoo_open = -1
		yahoo_close = -1
		yahoo_volume = -1
		google_open = -1
		google_close = -1
		google_volume = -1

		
		
		cursor.execute( " select open, close, volume from yahoo_scrape where date_id = " +str(date_id)+" and asset = \'"+str(asset)+"\'")
	    y_result = cursor.fetchone()
		if y_result != None:
			yahoo_open = y_result[0]
			yahoo_close = y_result[1]
			yahoo_volume = y_result[2]

	
		cursor.execute( " select open, close, volume from google_scrape where date_id = " +str(date_id)+" and asset = \'"+str(asset)+"\'")
	    g_result = cursor.fetchone()
		if g_result != None:
			google_open = g_result[0]
			google_close = g_result[1]
			google_volume = g_result[2]


	    avo = -1 
		if yahoo_open != -1 and google_open != -1:
	        	if eod_open == yahoo_open or eod_open == google_open:
		                avo = eod_open
				else:
			        if yahoo_open == google_open:
       			       	avo = google_open
		else:
			avo = eod_open

       	avc = -1
		if yahoo_close != -1 and google_close != -1:
       			if eod_close == yahoo_close or eod_close == google_close:
	               		avc = eod_close
				else:
			        if yahoo_close == google_close:
       			       	avc = google_open
		else:
			avc = eod_close
		
		error_cache = 0

		if avc == -1:
			print "No match for "+str(asset)+" CLOSE for "+str(date) 
			nomatch.write("No match for "+str(asset)+" CLOSE for "+str(date)+"\n")
		elif avc == 0:
			err.write(str(asset)+" CLOSE for "+str(date)+" is shit\n")
			error_cache = 1

       	elif avc !=  eod_close:
			f.write('update asset_value set close = '+str(avc)+' where asset = \''+str(asset)+'\' and date_id = '+str(date_id)+';\n')
			error_cache = 1
		if avo == -1:
			print "No match for "+str(asset)+" OPEN for "+str(date) 
			nomatch.write("No match for "+str(asset)+" OPEN for "+str(date)+"\n")
		elif avo == 0:
			err.write(str(asset)+" CLOSE for "+str(date)+" is shit\n")
			error_cache = 1

       	elif avo != eod_open:
			f.write('update asset_value set open = '+str(avo)+' where asset = \''+str(asset)+'\' and date_id = '+str(date_id)+';\n')
			error_cache = 1
		else: 
			tmp = 1
                	#print "passed "+str(asset)+" for "+str(date) 
		if error_cache == 1:
			errors.append([date_id, asset])			
	f.close()

err.close()
nomatch.close()



