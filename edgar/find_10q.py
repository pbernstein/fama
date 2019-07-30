#!/usr/bin/python
import sys
import re
import glob
import os
import shutil


#file = sys.argv[1]
#f = open("ford-10k.sgml")
#f = open(file)

xbrl_10q_list = []
xbrl_10k_list = []
#path = "/home/peter/work/edgar/data/forms/edgar/data/"
path = "/media/data/investments/data/edgar/forms"
q12012_path = "/media/data/investments/data/edgar/forms/2012q1"
q22012_path = "/media/data/investments/data/edgar/forms/2012q2"
all = 0
q10_counter = 0
xbrl_counter = 0
for file in sorted(glob.glob( os.path.join(path, '*.dat') )):
	f = open(file)	
	f10k = 0
	f10q = 0
	xbrl = 0
	q12012 = 0
	q22012 = 0
	result = ""
	all = all + 1
	for record in f:
		try:
			record.index("CONFORMED PERIOD OF REPORT")
#			print record[record.rindex("\t")+1:]

			if record[record.rindex("\t")+1:].find("20120331") != -1: q12012 = 1
			if record[record.rindex("\t")+1:].find("20120401") != -1: q12012 = 1

			if record[record.rindex("\t")+1:].find("20120631") != -1: q22012 = 1
			if record[record.rindex("\t")+1:].find("20120701") != -1: q22012 = 1
			#if q12012 == 1: print "found 10q"
		except:
			try:
				re.search("^<TYPE>10-Q$",record).group()
#				print "found 10q"
				f10q = 1
			except:
				if xbrl == 0:
					if record.find("<us-gaap:") != -1:
						#print "found xbrl"
						xbrl = 1

		if f10q == 1 and q12012 == 1 and xbrl == 1:	break

	#print f10q, q12012, xbrl
	if f10q == 1 and q12012 == 1:		
		#print file
		q10_counter = q10_counter + 1
		
	if f10q == 1 and q12012 == 1 and xbrl == 1:	
		print file
		xbrl_counter = xbrl_counter + 1
		shutil.move(file,q12012_path)

	if f10q == 1 and q22012 == 1 and xbrl == 1:	
		print file
		xbrl_counter = xbrl_counter + 1
		shutil.move(file,q22012_path)

	if f10q == 1 and q12012 == 1 and xbrl == 0:
		#print "not xbrl 10q:", file
		tmp = 1

#	if xbrl_counter == 5: break

	f.close()

print str(xbrl_counter)+" of "+ str(q10_counter) +" of "+ str(all)
