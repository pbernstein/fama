#!/usr/bin/python
	

from datetime import datetime
import sys
import re
import glob
import os

import MySQLdb
import buckets
import time
from time import strptime
import shutil
import send_generic_email_attachment as send_email
import boto


def s3_load(file,s3_name):
	
	s3 = boto.connect_s3()
	#bucket = s3.create_bucket('media.instrumental-data.com')  # bucket names must be unique
	bucket = s3.get_bucket('media.instrumental-data.com')
	key = bucket.new_key(s3_name)
	key.set_contents_from_filename(file,reduced_redundancy=True)
	key.set_acl('public-read') 
	#key.set_metadata('loadts',str(datetime.now()))



if __name__ == '__main__':
	file = sys.argv[1] 
	# where the file is on disk
	pieces = sys.argv[2].split("_")
	# expect s3_name to be "filings/2013-06-14/APPLE_10K.html" or something
	# expect s3_name to be "filings/2013-06-14/APPL_10K_20130401.html" or something
	s3_name = pieces[0]+"_"+pieces[1]
	print "s3 publishing "+s3_name
	s3_load(file,s3_name)
