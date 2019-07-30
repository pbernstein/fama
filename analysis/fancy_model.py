#!/usr/bin/python

import sys
import time
from datetime import datetime
import os
import os.path
from subprocess import call
import tweet
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

# SET GLOBALS

conn = db.get_conn()
cursor = conn.cursor()




# read in ins_map
#
# buy or sell the stock at the first open price after the filing
# check following opens until the end of the day
# 	if its on the wrong side of the price at initial action, get out, subtract from profit
#	else keep till the end of the day, reverse at last open price, add to profit
#
# print profit for each day




cursor.execute("""

select im.eh_sk, im.symbol, im.form, im.load_tsp, date_format(im.load_tsp, '%Y-%m-%d'),
im.value -  (  select p.value from ins_map p where im.symbol = p.symbol and im.attribute = p.attribute and im.form = p.form
and im.date_id > p.date_id order by p.date_id desc limit 1    )  as compare,

(  select e.eh_sk from extract_history e where im.cik = e.cik and im.date_id = e.date_id and e.form = '8-K' limit 1    )  as eightk_eh_sk,
(  select e.insert_ts from extract_history e where im.cik = e.cik and im.date_id = e.date_id and e.form = '8-K' limit 1    )  as eightk_tsp


im.value,
(  select p.value from ins_map p where im.symbol = p.symbol and im.attribute = p.attribute and im.form = p.form
and im.date_id > p.date_id order by p.date_id desc limit 1    )  as pre_value

from ins_map im where im.date_id > 8766
and im.attribute = 'Cash'
#and im.attribute = 'Revenues'
#and im.attribute = 'NetIncome'


and (  select p.value from ins_map p where im.symbol = p.symbol and im.attribute = p.attribute and im.form = p.form and im.date_id > p.date_id  order by p.date_id desc limit 1    )  is not null
and (  select e.eh_sk from extract_history e where im.cik = e.cik and im.date_id = e.date_id and e.form = '8-K' limit 1 ) is not null

""")
rows = cursor.fetchall()
enter = 0
exit = 0
total_profit = 0
capital = 10000
shares = 0

win_cnt = 0
lose_cnt = 0
for row in rows:
	eh_sk = str(row[0])
	symbol = row[1]
	enter = 0
	exit = 0
	form = row[2]
	load_tsp = str(row[3])
	date = str(row[4])
	compare = row[5]
	eight_eh_sk = str(row[6])
	eight_tsp = str(row[7])

	cursor.execute("select open from histprice where eh_sk = "+eh_sk+" and instant > '"+load_tsp+"' and instant < '"+date+" 16:00:00' order by instant ")
	prices = cursor.fetchall()
	if len(prices) == 0:
		continue
	if prices[0][0] < 10:
		continue

	cursor.execute("select open from histprice where eh_sk = "+eh_sk+" and instant > '"+eight_tsp+"'order by instant limit 1 ")
	eight_price = cursor.fetchone()[0]


	if prices[0][0] < eight_price:
		compare = -1
	else:
		compare = 1

	print "Working with "+symbol
	for order, price_tpl in enumerate(prices):
			price = price_tpl[0]
			#print order, price
			if order == 0:
				print "Enter the market at: "+str(price)
				enter = price
				continue
			#print "enter = "+str(enter)
			exit = price
			if compare > 0 and price < enter - .5 :
				break
			if compare < 0 and price > enter  - .5 :
				break

	print "Exit the market at: "+str(exit)
	shares = capital / enter
	if compare > 0:
		profit = (exit * shares )  - (enter * shares)
	else:
		profit = (enter * shares) - (exit * shares)

	print "profit = "+str(profit)
	if profit < 0:
		lose_cnt = lose_cnt + 1
	else:
		win_cnt = win_cnt + 1
	total_profit = total_profit + profit

print
print "Total profit = "+str(total_profit)
print "wins: "+str(win_cnt)
print "lose: "+str(lose_cnt)


