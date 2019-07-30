#!/usr/bin/python


import sys
import datetime
import os
import commands
import market_order as ma
import mktcls_order as moc
import mktopg_order as moo
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

#Initialize logging variables
    actions_log = []

# Initialize IB connections

    IBcon = ibConnection()
    IBcon.registerAll(watcher)
    printl("connect")
    IBcon.connect()
    sleep(2)



# Initiate new trades in the morning

    cursor.execute("select trade_sk, asset, exchange, shares, action from trade where trade_date_id = \""+str(date_id)+"\" and type = \"ENTER\" and status = 0")
    rows = cursor.fetchall()
    if len(rows) != 0:
       for row in rows:
		printl("Opening a trade")
                actions_log.append("Opening a trade")
		#print row
		trade_sk = row[0]
		asset = row[1]
		exchange = row[2]
		shares = row[3]
		action = row[4]

		printl("Placing a market on open order to "+str(action)+" "+str(shares)+" shares of "+str(asset))
		actions_log.append("Placing a market on open order to "+str(action)+" "+str(shares)+" shares of "+str(asset))
		# Place a moo order, Market On Open
		if exchange == "NASDAQ":
			moo.place_order(asset,action,shares,IBcon)
		else:
			ma.place_order(asset,action,shares,IBcon)  # Plain vanila market, NYSE AND AMEX only let you place MOO orders for lot sizes rounded to 100's
                IBcon.reqAccountUpdates(1,'') 


		# This is wrong. Fix later
		# PARSE OUTPUT in Market order,  figure out if it worked. IF it did
		cursor.execute("update trade set status = 1 where trade_sk = "+str(trade_sk))


# Reverse opening trades 

#    cursor.execute("select trade_sk, asset, shares, action from trade where trade_date_id = \""+str(date_id)+"\" and type = \"EXIT\" and status = 0")
    rows = cursor.fetchall()
    if len(rows) != 0:
       for row in rows:
		printl("Reversing a trade")
		actions_log.append("Reversing a trade")
		#print row
		trade_sk = row[0]
		asset = row[1]
		shares = row[2]
		action = row[3]

		printl("Placing a market on close order to "+str(action)+" "+str(shares)+" shares of "+str(asset))
		actions_log.append("Placing a market on close order to "+str(action)+" "+str(shares)+" shares of "+str(asset))
		# Place a moc order, Market On Close 
    		moc.place_order(asset,action,shares,IBcon)
                IBcon.reqAccountUpdates(1,'') 

		# This is wrong. Fix later
		# PARSE OUTPUT in Market order,  figure out if it worked. IF it did
		cursor.execute("update trade set status = 1 where trade_sk = "+str(trade_sk))

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

    to="notification email"
    log_path = "/home/ubuntu/work/trade_log/"
    attachment = commands.getoutput("ls -1 "+str(log_path)+"*.log | tail -1")
    error = commands.getoutput("grep \"Error\" "+str(log_path)+str(attachment)+" | grep -v \"Error id=-1\"")
    if len(actions_log) > 0:	
    	if len(error) > 0:
		subject=str(now)+" Trade Execution Report. CONTAINS ERROR"
       		body = "THERE WAS AN ERROR RETURNED DURING TODAY'S TRADING:\n"
	else:
		subject=str(now)+" Trade Execution Report"
		body = "Execution Summary:\n"	
	
        for i in range(len(actions_log)):
		body = body + actions_log[i] +"\n" 
    else:
	subject=str(now)+" Trade Execution Report: NO ACTIVITY"
	body = "Nothing to do today!"		
    ser.mail(to ,subject, body, attachment)


  
