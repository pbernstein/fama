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
	DESCRIPTION = 1
	TYPE = 1
	for record in file:
		if record.upper().find("<DESCRIPTION>") != -1:
			if record.upper().split("<DESCRIPTION>")[1].find("XBRL") != -1:
				DESCRIPTION = 0
			else:
				DESCRIPTION = 1
			
		if record.upper().find("<TYPE>") != -1:
			if record.upper().split("<TYPE>")[1].find("XML") != -1:
				TYPE = 0
			else:
				TYPE = 1
				
		if record.upper().find("</HTML>") != -1:
			write = 0
		if record.upper().find("<HTML>") != -1:
			write = 1
		if write == 1 and DESCRIPTION == 1 and TYPE == 1 or record.upper().find("</HTML>") != -1:
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

