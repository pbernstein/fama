#!/usr/bin/python

import os
import glob
from multiprocessing import Lock
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

# SET GLOBALS
conn = db.get_conn()
cursor = conn.cursor()


from time import strptime

from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
#from requestHistoricalData import *
import os.path, time
import sys

from history_tick_scrape import populate_price as pop 


def execute():
    print "in execute"
    cursor.execute("select date_id, asset from daily_returns where amount = 30000 and fama_offset = 30 and min_alpha = 0.0025 and min_sig = 2 and min_assets = 1 and max_assets = 20 and duration = 4 and date_id > 8797")
    rows = cursor.fetchall()
    for row in rows:
        if not os.path.isfile('/home/peter/work/scraping/hist_extract'):
            print "No /home/peter/work/scraping/hist_extract file. Exiting"
            sys.exit(0)

        date_id = str(row[0])
        cursor.execute("select date from dates where date_id = "+date_id)
        date = str(cursor.fetchone()[0])
        symbol = row[1]
        print date, symbol
        os.system('/home/peter/work/scraping/history_tick_scrape.py '+symbol+' '+date+' BID')
        os.system('/home/peter/work/scraping/history_tick_scrape.py '+symbol+' '+date+' ASK')
        os.system('/home/peter/work/scraping/history_tick_scrape.py '+symbol+' '+date+' TRADES')




if __name__ == "__main__": execute()


cursor.close()
conn.commit()
conn.close()

