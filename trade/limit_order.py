#! /usr/bin/env python

from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import ibConnection, message
from time import sleep
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

# SET GLOBALS




def watcher(msg):
    print msg

def makeStkContract(sym):
    contract = Contract()
    contract.m_symbol = sym
    contract.m_secType = 'STK'
    contract.m_exchange = 'SMART'
    contract.m_primaryExch = 'SMART'
    contract.m_currency = 'USD'
    contract.m_outsideRth = True
    contract.m_localSymbol = sym
    return contract

def makeStkOrder(shares,action,price):
    order = Order()
    order.m_minQty = shares
    order.m_lmtPrice = price
    order.m_orderType = 'LMT'
    order.m_totalQuantity = shares
#    order.m_outsideRth = True
    order.m_action = str(action).upper()
    return order

def printl(self):
	print self
	sys.stderr.write(self+"\n")

def place_order(sym, action, shares,price,con):

# Generate a new Order ID. I do this becuase you can't call query the API for NextOrderId in rapid succession

    DBconn = db.get_conn()
    cursor = DBconn.cursor()
    cursor.execute("insert into orderID_gen (request) values (1)")
    cursor.execute("select max(orderID) from orderID_gen")
    result = cursor.fetchone()
    orderID = result[0]
 
    print "Placing orderID: "
    print "Symbol: "+str(sym)
    print "Action: "+str(action)
    print "Shares: "+str(shares)
    print "Price: "+str(price)
    
    printl("Create contract")
    stkContract = makeStkContract(sym) 
    printl("Create order")
    stkOrder = makeStkOrder(shares, action, price)
    printl("place order")
    con.placeOrder(orderID, stkContract, stkOrder)
    sleep(2)
    print "Order placed"


if __name__ == '__main__':
    sym = sys.argv[1]
    action = sys.argv[2]
    shares = sys.argv[3]
    price = sys.argv[4]
    con = sys.argv[5]
    place_order(sym, action,shares,price,con)
	


