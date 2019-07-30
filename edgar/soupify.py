#!/usr/bin/python


import sys
import re
import glob
import os
import shutil
import MySQLdb
import ho.pisa as pisa
from BeautifulSoup import BeautifulSoup




def file_get_contents(filename):
    with open(filename) as f:
        return f.read()


soup = BeautifulSoup(file_get_contents("/media/data/investments/data/edgar/forms/rss/error/msah-20120630.xml"))

cache = ""
count = 0
for i in soup.prettify().split("\n"):
	if count == 1:
		count = 2
		cache = cache + i
		continue
	elif count == 2:
		count = 0
		payload = cache + i
		print payload.replace(" ","")
		continue
	elif i.find("instant>") != -1 or i.find("startdate>") != -1 or i.find("enddate>") != -1 or i.find("measure>") != -1 or i.find("<us-gaap:") != -1:
		count = 1
		cache = i
		continue
	else:
		print i






		
