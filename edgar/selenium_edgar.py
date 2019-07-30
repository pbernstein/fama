#!/usr/bin/python


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import os
import sys
random.seed()
from subprocess import call
from datetime import datetime



def get_filing(base_url,cik,name):
	os.environ['DISPLAY'] = ':0'
	file_date = str(datetime.today().date())
	html_path = "/media/data/investments/data/edgar/forms/rss/loaded/html/"+file_date+"/"+str(cik)
	fn =  html_path+'/'+name+'_8-K.html'
	print html_path
	fp = webdriver.FirefoxProfile("/home/peter/.mozilla/firefox/jamj5bx8.default/")
	driver = webdriver.Firefox(firefox_profile=fp)
	driver.get(base_url)
	driver.find_elements_by_xpath(".//html/body/form[@id='form1']/table[2]/tbody/tr[1]/td[2]/table/tbody/tr/td/table/tbody/tr")[2].click()
	sleep(int(random.random()*10) % 5)

	count = 0
	while True:
		count = count + 1
		try:
			driver.switch_to_frame("nav")
			sleep(int(random.random()*10) % 5)
			break
		except:
			if count == 10:
				driver.close()
				return 0,fn
				break
			sleep(int(random.random()*10) % 5)

	print "in nav"
	count = 0
	while True:
		count = count + 1
		try:
			driver.find_element_by_id('disFilingInfoDet_hlVEntFiling').click()
			sleep(int(random.random()*10) % 5)
			break
		except:
			if count == 10:
				driver.close()
				return 0,fn
				break
			sleep(int(random.random()*10) % 5)

	print "in clicked"


	count = 0
	while True:
		count = count + 1
		try:
			driver.switch_to_frame("filing")
			sleep(int(random.random()*10) % 5)
			break
		except:
			if count == 10:
				driver.close()
				return 0,fn
				break
			sleep(int(random.random()*10) % 5)

	print "in filing"

	try:
		page = driver.page_source
		call(["mkdir","-p",html_path])
		f = open(fn,'w')
		#print "ready to write to "+fn
		for line in page.split("\n"):
				try:
					f.write(line+"\n")
				except:
					try:
						for char in line:
							try:
								f.write(char)
							except:
								f.write("\n")
						f.write("\n")
					except:
						#f.write("can't even print the first character!\n")
						pass
		f.close()

	except:
		print "failed in extract"
		driver.close()
		return 0,fn


		
	driver.close()
	return 1,fn


if __name__ == '__main__':
        base_url= sys.argv[1]
        success = get_filing(base_url)
	print "success is: "+str(success)

