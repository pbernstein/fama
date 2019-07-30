#!/usr/bin/python


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import os
random.seed()

# ff profile: ~/.mozilla/firefox/iik6utkf.default/

fp = webdriver.FirefoxProfile("/home/peter/.mozilla/firefox/iik6utkf.default")
driver = webdriver.Firefox(firefox_profile=fp)

f = open('/home/peter/work/scraping/nyse.list')
equities = []
for row in f:
        equities.append(row.replace("\n",""))

#equities = ["ARBA"]
equities = [["AAPL","NASDAQ"]]

for equity in equities:
	while 1:
                if os.path.exists("/home/peter/work/edgar/advfn_scrape"):
                        break;
                else:
                        sleep(10)

	symbol = equity[0]
	exchange = equity[1]
	base_url = "http://www.advfn.com/p.php?pid=financials&btn=start_date&mode=annual_reports&symbol="+exchange+"%3A"+str(symbol)
	driver.get(base_url)

	dates =  ['2001/03','2002/06','2003/09','2004/12','2006/03','2007/06','2008/09','2009/12','2011/03','2012/06']
	for date in dates:
		#print "|"+date+"|"
		try:
			elem = driver.find_element_by_name("istart_date")
		except:
			continue

		for option in elem.find_elements_by_tag_name('option'):
			#print "|"+option.text+"|"
		 	if option.text == date:
		        	option.click()
				break

		#sleep(int((random.random()*10) % 5)/2)
		current_url = driver.current_url # tells us the current url
		#print "url = "+str(url)
		if current_url != base_url:
			str_date = date.replace("/","-")
			#print "wget -O /media/data/investments/data/historic/"+str(equity)+"_"+str(str_date)+".dat '"+current_url+"'; sleep $(( $RANDOM % 3 + 1));"
			html_source = fp.page_source
			o = open("/media/data/investments/data/historic/"+str(symbol)+"_"+str(str_date)+"_10K.dat")
			for line in html_source:
				o.write(line)
			o.close()


		sleep(int(random.random()*10) % 5)
		break

driver.close()

