#!/usr/bin/python
# Arguments:  manually_place.py GOOG BUY 1


import sys
import datetime
import os
import market_order as ma
import send_email_report as ser
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import ibConnection, message
from time import sleep
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

def watcher(msg):
    print msg

def UpdatePortfoliowatcher(msg): 
    print 'UpdatePortfolioWatcher %s : %s %s' % (datetime.datetime.now(), msg.contract.m_symbol,msg.position ) 



def printl(self):
        print self
        sys.stderr.write(self+"\n")

if __name__ == '__main__':

    sym = sys.argv[1]
    action = sys.argv[2]
    shares = sys.argv[3]


# Derive Date
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M")[:10]

# Initialize log files
    printl("Starting execute at "+str(now))

# Set up MYSQL connection
    DBconn = db.get_conn()
    cursor = DBconn.cursor()

# Derive date_id
    cursor.execute("select date_id from dates where date = \'"+str(date)+"\'")
    result = cursor.fetchone()
    date_id = result[0]

#    print date_id    
#    date_id = 4012


# Initialize IB connections

    printl("initialize IbPy connection")
    IBcon = ibConnection()
    printl("registerAll")
    IBcon.registerAll(watcher)
#    IBcon.register(UpdatePortfoliowatcher,'UpdatePortfolio')
    printl("connect")
    IBcon.connect()
    sleep(2)


# Reverse trades made earlier that day

     
#  Keep a log of your trade
    print "insert into trade (trade_date_id, asset, action, shares, status, type) values (\""+str(date_id)+"\",\""+str(sym)+"\",\""+str(action)+"\","+str(shares)+",3,\"MANUAL\")"
    cursor.execute("insert into trade (trade_date_id, asset, action, shares, status, type) values (\""+str(date_id)+"\",\""+str(sym)+"\",\""+str(action)+"\","+str(shares)+",3,\"MANUAL\")")
    cursor.execute("select trade_sk from trade where trade_date_id = \""+str(date_id)+"\" and asset = \""+str(sym)+"\" and action = \""+str(action)+"\" and shares = "+str(shares)+" and status = 3 and type = \"MANUAL\"")

# EXAMPLE:
# select trade_sk, asset, shares, action from trade where trade_date_id = 4021 and type = "EXIT" and status = 0 and asset in (select asset from trade where trade_date_id = 4021 and status = 1)



    rows = cursor.fetchall()
    if len(rows) != 0:
       for row in rows:
		printl("Executing trade")
		printl("Placing trade to "+str(action)+" "+str(shares)+" shares of "+str(sym))
    		ma.place_order(sym,action,shares,IBcon)
                ma_result = IBcon.reqAccountUpdates(1,'') 

		# PARSE OUTPUT in Market order,  figure out if it worked. IF it did
		cursor.execute("update trade set status = 4 where trade_sk = "+str(row[0]))


# Close IB Connection

    printl("disconnect")
    IBcon.disconnect()
    sleep(2)



# Commit and Close MYSQL connections
    cursor.close()
    DBconn.commit()
    DBconn.close()


    now = datetime.datetime.now()
    print "Successfully exiting execute at "+str(now)

  
