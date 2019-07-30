#!/usr/bin/python


import sys
import re
import glob
import os
import shutil
import MySQLdb
from BeautifulSoup import BeautifulSoup




def clean(file):
	cache = ""
	write = 0
	count = 0
	TYPE = 0
	DESCRIPTION = 0
	output = []
	for record in file:
		if record.find("<DESCRIPTION>") != -1:
			if record.find("<DESCRIPTION>XBRL INSTANCE DOCUMENT") != -1:
				DESCRIPTION = 1
			else:
				DESCRIPTION = 0
			
		if DESCRIPTION == 1:
			#print record
			output.append(record)
		#print record
		#print write, DESCRIPTION, TYPE



	return output

if __name__ == '__main__':
	file = open(sys.argv[1])
	data = clean(file)
	for i in data:
		print i

