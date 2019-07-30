#!/usr/bin/python

import sys
import os
import time
import investments as inv
import send_generic_email_attachment
import day_return as dayr
import operator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

with open('../config.json') as config_file:
    data = json.load(config_file)


def main(amount, process_date, duration = 0, fama = 0, alpha = 0, sig = 0, mi = 0, ma = 0, sendmail = "N"):
	permutations = []
 	profit = 0
 	sell_profit = 0
	buy_assets = []
	sell_assets = []
        ra_conn = db.get_conn()
        ra_cursor = ra_conn.cursor()



        ra_cursor.execute ("SELECT date_id, day_of_week, month_day, month_num, year from dates where date = \""+str(process_date)+"\"")
        row = ra_cursor.fetchall()
        date_id = row[0][0]
        dow = row[0][1]
        md = row[0][2]
        mn = row[0][3]
        year = row[0][4]


	do_not_go = 0

        ra_cursor.execute ("SELECT d.date_id, sum(dr.profit) from daily_returns dr, dates d where d.date_id  = dr.date_id and d.month_num = "+str(mn)+" and d.year = "+str(year)+" and d.month_day < "+str(md)+" and dr.amount = "+str(amount)+" and dr.duration = "+str(duration)+" and dr.fama_offset = " +str(fama)+" and dr.min_alpha = "+str(alpha)+" and dr.min_sig = "+str(sig)+" and dr.min_assets = "+str(mi)+" and dr.max_assets = "+str(ma)+" group by d.date_id")
	rows = ra_cursor.fetchall()
	month_total = 0
#	if float(month_total) > (float(int(amount)*.066) * -1):   # If I've already lost 6.6% of my investment so far this month
	for row in rows:
		if row[1] != None:
			month_total = month_total + row[1] 	
			if month_total < (float(int(amount)*.066) * -1):
				do_not_go = 1
				break

	junk_list1 = []
	junk_list2 = []
	if do_not_go == 0:
		buy_assets, sell_assets, profit =  dayr.day_return(amount,process_date,duration,fama,alpha,sig,mi,ma, "Y")
	perm =[duration, fama, alpha, sig, mi,ma]



        ra_cursor.close()


	buy_string = "|".join(map(str,buy_assets))	
	sell_string = "|".join(map(str,sell_assets))	
	print buy_string
	print sell_string
	if sendmail == "Y":
		print "sending email"
		header = " ".join(map(str,[process_date, duration, fama, alpha, sig, mi, ma]))
		send_email.main(data.gmail_user, str(process_date), header, buy_string, sell_string)
	else:
		print str(process_date), str(dow).ljust(9), str(perm), str(round(float(profit),2)).ljust(8)
		return (profit)


if __name__ == '__main__':
	amount = sys.argv[1]		# How much to invest 
	process_date = sys.argv[2]	# prediction date
        duration = sys.argv[3]          # How many days of history to regress against
	fama_offset = sys.argv[4]       # How many days ago to join the fama data to the asset value
        min_alpha = sys.argv[5]         # minimal alpha to be included in portfolio
	min_sig = sys.argv[6]           # minimal signifigance to be included in portfolio
        min_assets = sys.argv[7]        # Min Assets in a porfolio  ( do not enter the market that day if you cannot construct a portfolio with this many assets)
	max_assets = sys.argv[8]        # Max Assets in a portfolio
	if len(sys.argv) > 9:
       		sendmail = sys.argv[9]  # optional parameter to send an email
	else:	
		sendmail = "N"
       	main(amount, process_date, duration, fama_offset, min_alpha, min_sig, min_assets, max_assets, sendmail)

