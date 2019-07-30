#!/usr/bin/python


import sys
import os
import re
from BeautifulSoup import BeautifulSoup

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()


def cleanse(filename,symbol):
        #soup = BeautifulSoup(file_get_contents(filename))
        temp_filename = filename+".temp"
        cleansed_filename = filename+".cleansed"
        temp_out = open(temp_filename,'w')
        out = open(cleansed_filename,'w')
	custom_tag_list = [symbol, "dei"]
        cache = ""
        count = 0
        #for i in soup.prettify().split("\n"):
	for i in open(filename):		
		payload = i
		for custom_tag in custom_tag_list:
			if payload.find("<"+custom_tag.lower()+":") != -1:
				payload = payload.lower().replace("<"+custom_tag.lower()+":","<us-gaap:")
				payload = payload.lower().replace("</"+custom_tag.lower()+":","</us-gaap:")

		"""
		# This is wrong, i am converting EVERYTHING to us-gaap, which is overkill, the system above is better

		cache = i.lower()	
		custom_open_tag =  re.match("^[a-z0-9].+$",cache[cache.index("<")+1:cache.index(":")])
		custom_close_tag =  re.match("^[a-z0-9].+$",cache[cache.rindex("</")+2:cache.rindex(":")])
		if custom_open_tag != None and custom_close_tag != None:
			if custom_open_tag == custom_close_tag:
			cache = cache.replace
		"""			

	
	
		temp_out.write(payload+"\n")
	temp_out.close()			

	#for i in open(filename):
	for i in open(filename+".temp"):


# Not working for:
# <xbrli:context id="I2012Q3">
#    <xbrli:entity>
#      <xbrli:identifier scheme="http://www.sec.gov/CIK">0000070858</xbrli:identifier>
#    </xbrli:entity>
#    <xbrli:period>
#      <xbrli:instant>2012-09-30</xbrli:instant>
#    </xbrli:period>
#  </xbrli:context>
		if i.lstrip().rstrip() == "":
			continue
			

		#print "i = "+str(i)
		if	(i.lower().find("</us-gaap:") != -1 and i.lower().find("<us-gaap:") != -1) or  \
			(i.lower().find("</xbrli:us-gaap:") != -1 and i.lower().find("<xbrli:us-gaap:") != -1) or  \
			(i.lower().find("/instant>") != -1 and i.lower().find("<instant") != -1) or  \
			(i.lower().find("/xbrli:instant>") != -1 and i.lower().find("<xbrli:instant") != -1) or  \
			(i.lower().find("/enddate>") != -1 and i.lower().find("<enddate") != -1)  or \
			(i.lower().find("/xbrli:enddate>") != -1 and i.lower().find("<xbrli:enddate") != -1)  or \
			(i.lower().find("/startdate>") != -1 and i.lower().find("<startdate") != -1) or \
			(i.lower().find("/xbrli:startdate>") != -1 and i.lower().find("<xbrli:startdate") != -1) or \
			(i.lower().find("/measure>") != -1 and i.lower().find("<measure") != -1)  or \
			(i.lower().find("/xbrli:measure>") != -1 and i.lower().find("<xbrli:measure") != -1):

			payload = i.lower()
			#payload = i
			out.write(payload+"\n")
			cache = ""
			count = 0
			continue
                if count == 1:
                        count = 2
                        cache = cache.lstrip().rstrip() + i.lstrip().rstrip()
                        continue
                elif count > 1:
			if 	i.lower().find("/instant>") != -1 or i.lower().find("/startdate>") != -1 or i.lower().find("/enddate>") != -1 or i.lower().find("/measure>") != -1 or i.lower().find("</us-gaap:") != -1 or \
				i.lower().find("/xbrli:instant>") != -1 or i.lower().find("/xbrli:startdate>") != -1 or i.lower().find("/xbrli:enddate>") != -1 or i.lower().find("/xbrli:measure>") != -1 or i.lower().find("</xbrli:us-gaap:") != -1:

	                        count = 0
       		                payload = cache + i.lstrip()
                        	out.write(payload+"\n")
				#print payload.replace(" ","")
				#out.write(payload.lstrip().rstrip()+"\n")
                	elif 	i.lower().find("instant>") != -1 or i.lower().find("startdate>") != -1 or i.lower().find("enddate>") != -1 or i.lower().find("measure>") != -1 or i.lower().find("<us-gaap:") != -1 or \
                		i.lower().find("xbrli:instant>") != -1 or i.lower().find("xbrli:startdate>") != -1 or i.lower().find("xbrli:enddate>") != -1 or i.lower().find("xbrli:measure>") != -1 or i.lower().find("<xbrli:us-gaap:") != -1:
				# WTF? This tag had no close! Start over!
                        	cache = i
				count = 1
			else:
	                        cache = cache + i.lstrip().rstrip()
                        continue
                elif 	i.lower().find("instant>") != -1 or i.lower().find("startdate>") != -1 or i.lower().find("enddate>") != -1 or i.lower().find("measure>") != -1 or i.lower().find("<us-gaap:") != -1 or \
                	i.lower().find("xbrli:instant>") != -1 or i.lower().find("xbrli:startdate>") != -1 or i.lower().find("xbrli:enddate>") != -1 or i.lower().find("xbrli:measure>") != -1 or i.lower().find("<xbrli:us-gaap:") != -1:
                        count = 1
                        cache = i
                        continue
                else:
                        out.write(i.lower()+"\n")
        out.close()
        return cleansed_filename



if __name__ == '__main__':
        fn = sys.argv[1]
        symbol = sys.argv[2]
        cleanse(fn, symbol)



