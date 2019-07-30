#!/usr/bin/python


import sys
import os
import re
from BeautifulSoup import BeautifulSoup

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()


def html_cleanse(filename):
        soup = BeautifulSoup(file_get_contents(filename))
        temp_filename = filename+".temp"
        cleansed_filename = filename+".cleansed"
        out = open(cleansed_filename,'w')
	write = 0
	#for i in open(filename):		
	pretty = soup.prettify().split("\n")
	for i in pretty:
		#out.write(i+"\n")	
		#"""
		payload = i.replace("&"," and ")
		if i.find('<table border="0" bgcolor="ffffff" cellspacing="1" cellpadding="2" width="705" align="left">') != -1:
			write = 1
		if write == 1:	
			out.write(payload+"\n")
		if i.find("All amounts in") != -1:
			out.write(payload+"\n")
		if i.find('</table>') != -1:
			write = 0
			
		#"""

	out.close()
	
        return cleansed_filename



if __name__ == '__main__':
        fn = sys.argv[1]
        html_cleanse(fn)



