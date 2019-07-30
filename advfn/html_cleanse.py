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
	pretty = soup.prettify().split("\n")
	for i in pretty:
		#out.write(i+"\n")	

		#"""
		payload = i.replace("&"," and ")


		if i.find('<table') != -1 and i.find('border="0"') != -1 and i.find('bgcolor="ffffff"') != -1 and i.find('cellspacing="1"') != -1 and i.find('cellpadding="2"' ) != -1 and i.find('width="705"' ) != -1 and i.find('align="left"') != -1:





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



