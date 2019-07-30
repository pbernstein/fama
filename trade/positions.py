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

def UpdatePortfoliowatcher(msg):
    print 'POSITIONS : %s : %s %s' % (datetime.datetime.now(), msg.contract.m_symbol,msg.position )


def printl(self):
        print self
        sys.stderr.write(self)

if __name__ == '__main__':

    IBcon = ibConnection()
    IBcon.register(UpdatePortfoliowatcher,'UpdatePortfolio')
#    IBcon.registerAll(watcher)
    IBcon.connect()
    sleep(2)
    IBcon.reqAccountUpdates(1, '')
    sleep(2)
    IBcon.disconnect()
    sleep(2)


