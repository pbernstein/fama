#!/usr/bin/python

import sys
import datetime
import os
import send_email_report as ser
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import ibConnection, message
from time import sleep


def watcher(msg):
    print msg

#def OpenOrdersWatcher(msg):
#    # Research documentation for "OpenOrder"
##    print 'OpenOrdersWatcher %s : %s ' % (datetime.datetime.now(), msg.contract.m_symbol )
#    print 'OPEN ORDERS:  %s : %s %s %s %s %s %s' % (datetime.datetime.now(), msg.orderId, msg.contract.m_symbol, msg.order.m_action, msg.order.m_totalQuantity, msg.order.m_tif, msg.order.m_orderType)
##    print msg
#
def UpdatePortfoliowatcher(msg):
#    print 'UpdatePortfolioWatcher %s : %s %s %s' % (datetime.datetime.now(), msg.contract.m_symbol,msg.position, msg.marketPrice )
	print '%s : %s %s %s' % (datetime.datetime.now(), msg.contract.m_symbol,msg.position, msg.marketPrice )
	if  msg.position > 0:
		print "I own "+str(msg.contract.m_symbol)
	if  msg.position < 0:
		print "I owe "+str(msg.contract.m_symbol)




def printl(self):
        print self
        sys.stderr.write(self)

if __name__ == '__main__':

    IBcon = ibConnection()
#    IBcon.register(UpdatePortfoliowatcher,'UpdatePortfolio')
    IBcon.register(UpdatePortfoliowatcher,'UpdatePortfolio') 
#    IBcon.registerAll(watcher)  

    IBcon.connect()
    IBcon.reqAccountUpdates(1, '')
#    IBcon.reqOpenOrders()
    IBcon.disconnect()
    sleep(2)


