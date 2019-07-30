#!/usr/bin/python

import os
import glob
from multiprocessing import Lock



from time import strptime

from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
#from requestHistoricalData import *
import os.path, time
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

# SET GLOBALS
conn = db.get_conn()
cursor = conn.cursor()


#bar_length = "15 secs"
#duration = "1800"
bar_length = "1 min"
duration = "28800"
type ='TRADES'
type = ''
tiny_type = ''
date_id = ''



order_ids = [0]
#eh_sk_mapping = {}
#symbol_mapping = {}
symbol_sk_mapping = {}
d = Lock()



def next_order_id():
    return order_ids[-1]


def save_order_id(msg):
    order_ids.append(msg.orderId)



def contract(contractTuple):
    newContract = Contract()
    newContract.m_symbol = contractTuple[0]
    newContract.m_secType = contractTuple[1]
    newContract.m_exchange = contractTuple[2]
    newContract.m_currency = contractTuple[3]
    #newContract.m_expiry = contractTuple[4]
    newContract.m_expiry = '1'
    newContract.m_strike = contractTuple[5]
    newContract.m_right = contractTuple[6]
    print 'Contract Parameters: [%s,%s,%s,%s,%s,%s,%s]' % contractTuple
    return newContract

# convert UTC to New York EST timezone
def ESTtime(msg):
    return time.gmtime(int(msg.date) - (5 - time.daylight)*3600)
#    return time.gmtime(int(msg.date))


# convert UTC to CST timezone
def CSTtime(msg):
    return time.gmtime(int(msg.date) - (6 - time.daylight)*3600)

def printData(msg):

    global d
  
    global symbol_sk_mapping
    global tiny_type
    global date_id

 
    if int(msg.high) > 0:
		dataStr =  '%s,%s,%s,%s,%s,%s' % (time.strftime('%Y,%m,%d,%H,%M,%S',
                                                        CSTtime(msg)),
                                          msg.open,
                                          msg.high,
                                          msg.low,
                                          msg.close,
                                          msg.volume)
	
		# inherit global eh_sk and bar_length

		instant = time.strftime('%Y-%m-%d %H:%M:%S',  CSTtime(msg))

		o = str(msg.open)
		h = str(msg.high)
		l = str(msg.low)
		c = str(msg.close)
		v = str(msg.volume)
    		d.acquire()
		#eh_sk = str(eh_sk_mapping[msg.reqId])
		symbol_sk = str(symbol_sk_mapping[msg.reqId])
		d.release()
    		d.acquire()
		#symbol = str(symbol_mapping[eh_sk])
		d.release()


		"""
		  `symbol` varchar(10) DEFAULT NULL,
		  `eh_sk` int(11) NOT NULL,
		  `price_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
		  `open` double DEFAULT NULL,
		  `high` double DEFAULT NULL,
		  `low` double DEFAULT NULL,
		  `price` double DEFAULT NULL,
		  `volume` double DEFAULT NULL,
		"""

		cursor.execute("insert into histprice (`date_id`,`symbol_sk`,`bar_length`,`type`, `instant`,`open`,`high`,`low`,`close`,`volume`) values ("+date_id+",'"+symbol_sk+"','"+bar_length+"','"+tiny_type+"','"+str(instant)+"',"+o+","+h+","+l+","+c+","+v+")")
	

    else:
        printData.finished = True

def watchAll(msg):
	if str(msg).find("162 - Historical Market Data") != -1:
		time.sleep(11*60)




def populate_price(symbol, date,type,tiny_type):
	
		global d

		global symbol_sk_mapping
          
        global duration
        global bar_length
        global date_id

        cursor.execute("select date_id from dates where date = '"+date+"'");
        date_id = str(cursor.fetchone()[0])


        cursor.execute("select symbol_sk from symbol where symbol = '"+symbol+"' and current = 1");
		symbol_sk = cursor.fetchone()[0]


        cursor.execute("select symbol_sk from histprice where symbol_sk = "+str(symbol_sk)+" and date_id = "+str(date_id)+" and type = '"+tiny_type+"'");
        try:
        		symbol_sk = cursor.fetchone()[0]
                print "already loaded"
                return
        except:
                print "not already loaded, pulling "+type
                os.system('sleep 10')
                pass



		#con = ibConnection()
		con = ibConnection('localhost', 4001, 0)
		con.clientId = 2
		con.registerAll(watchAll)
		#con.unregister(watchAll, message.historicalData)
		con.register(printData, message.historicalData)
		con.register(save_order_id, 'NextValidId')
		con.connect()
		time.sleep(1)
		counter = next_order_id()
		
		
		
		
		
		
		print symbol
		d.acquire()
		d.release()
    	d.acquire()
		symbol_sk_mapping[counter] = symbol_sk
		d.release()
		contractTuple = (symbol, 'STK', 'SMART', 'USD', '', 0.0, '')

        print date
    	year = date.split("-")[0]
        month = date.split("-")[1]
        day = date.split("-")[2] 
		requestTime = str(year)+str(month).zfill(2)+str(day).zfill(2)+" 17:01:01 EST" # This is the END time of the request
		print "Requesting: "+requestTime 
		newRowData = []
		printData.finished = False # true when historical data is done
		con.reqHistoricalData(counter,
			contract(contractTuple),
			requestTime, # last requested bar date/time
			duration+' S',  # quote duration, units: S,D,W,M,Y # 2 hours is 7200, 4 hours is 14400
			bar_length,  # bar length
			type,
			0, 2 )
		time.sleep(5)
		counter = counter + 1
		con.disconnect()





if __name__ == "__main__":
        symbol = sys.argv[1]
        date = sys.argv[2] # YYYY-MM-DD
        type = sys.argv[3] # YYYY-MM-DD
        if type == 'TRADES':
                tiny_type = 'T'

        if type == 'ASK':
                tiny_type = 'A'

        if type == 'BID':
                tiny_type = 'B'
	populate_price(symbol,date,type,tiny_type)

cursor.close()
conn.commit()
conn.close()


