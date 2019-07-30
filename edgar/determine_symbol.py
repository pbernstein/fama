#!/usr/bin/python

#
# Usage:
#  extract_quarter.py  2005 3 


import sys
import os
import os.path
import xbrl_load_quarter
import shutil
import MySQLdb
from subprocess import call
from datetime import datetime


def determine_symbol(file):
	"""
	I walk through the whole file, and look for this pattern:
	"<[a-z]:"
	The pattern that occurs the most often, that is not one that I'm expecting, like "us-gaap", i interpret as the symbol
	"""


	tag = []
	tag_count = {}
	found_tag = ""
	for line in file:
		try:
			if line.find("<") != -1 and line.find(":") != -1:
				if line.index("<") < line.index(":"):
					found_tag = line[line.index("<")+1:line.index(":")]
					if found_tag.find(" ") != -1:
						found_tag = ""
						continue
			try:
				tag_count[found_tag] =  tag_count[found_tag]  + 1
			except:
				tag_count[found_tag] = 0
			found_tag = ""
		except:
			found_tag = ""
			pass
	try:
		del tag_count[""]
	except:
		pass
	try:
		del tag_count["link"]
	except:
		pass
	try:
		del tag_count["us-gaap"]
	except:
		pass
	for key_list in tag_count.keys():
		if key_list.find("xbrl") != -1:
			del tag_count[key_list]

	for i in tag_count:
		tag.append([i,tag_count[i]])
	tag.sort(key=lambda r: r[1], reverse=True)
	return(tag[0][0])




local_fn = sys.argv[1]
symbol = determine_symbol(local_fn)

print symbol
