#!/usr/bin/python

import MySQLdb
import sys
import datetime
import os
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import ibConnection, message
from time import sleep


def watcher(msg):
    print msg

def UpdatePortfoliowatcher(msg): 
#    print 'UpdatePortfolioWatcher %s : %s ' % (datetime.datetime.now(), msg.values() )
#    print 'UpdatePortfolioWatcher %s : %s : %s ' % (datetime.datetime.now(), msg.values()[0], msg.values()[1] )
    if msg.values()[0] == "TotalCashBalance" and msg.values()[2] == "USD":
        print 'Cash Balance|%s|%s' % ( datetime.datetime.now(), msg.values()[1] )
	print
    
    if msg.values()[0] == "RegTEquity" and msg.values()[2] == "USD":
        print 'Total Value |%s|%s' % ( datetime.datetime.now(), msg.values()[1] )
	print

    if msg.values()[0] == "StockMarketValue" and msg.values()[2] == "USD":
        print 'Stock Market Value |%s|%s' % ( datetime.datetime.now(), msg.values()[1] )
	print


def printl(self):
        print self
        sys.stderr.write(self+"\n")

def test_print():
        print test

if __name__ == '__main__':


    IBcon = ibConnection()
    IBcon.register(UpdatePortfoliowatcher, 'UpdateAccountValue')
    #IBcon.registerAll(watcher)
    IBcon.connect()
    sleep(2)
    IBcon.reqAccountUpdates(1,'') 
# Close IB Connection
    IBcon.disconnect()
    sleep(2)
  
