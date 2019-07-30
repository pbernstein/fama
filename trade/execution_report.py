#!/usr/bin/python

import sys
import datetime
import os
import send_email_report as ser
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import ibConnection, message
from time import sleep
from ib.ext.ExecutionFilter import ExecutionFilter
from ib.opt import ibConnection


def watcher(msg):
    print msg.execution

def UpdatePortfoliowatcher(msg):
    print 'POSITIONS : %s : %s %s' % (datetime.datetime.now(), msg.contract.m_symbol,msg.position )

def ExecutionDetailsHandler(msg):
#    EXEC_DETAILS[msg.orderId] = msg.execution.shares
    EXEC_DETAILS[msg.orderId] = [msg.execution.m_price, msg.execution.m_side, msg.execution.m_shares, msg.contract.m_symbol, msg.execution.m_time ]

#-- factories ----------------------------
def makeExecFilter():
    filter=ExecutionFilter()
    return filter               


def start_tracking_Executions():
    filter=makeExecFilter()
    IBcon.reqExecutions(filter)


def printl(self):
        print self
        sys.stderr.write(self)




# global dict of orderId : Execution
#EXEC_DETAILS = {20261}                                                                             
EXEC_DETAILS = {}                                                                             



if __name__ == '__main__':

    IBcon = ibConnection()


   #con.registerAll(watcher)
    IBcon.register(ExecutionDetailsHandler, 'ExecDetails')
    IBcon.connect()
    sleep(2)

    filter=makeExecFilter()
    IBcon.reqExecutions(filter)
    sleep(2)                                                                                      
    for orderId in EXEC_DETAILS:
        print orderId, EXEC_DETAILS[orderId]


    IBcon.disconnect()
    sleep(2)                                                                                      
