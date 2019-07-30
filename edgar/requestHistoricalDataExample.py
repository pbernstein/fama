#!/usr/bin/env python
# -*- coding: utf-8 -*-

# requests historical data from TWS and can save to a CSV file

# bar length is set to 5 minute bars

# legal bar lengths: 1 secs, 5 secs, 10 secs, 15 secs, 30 secs, 1 min,
#     2 mins, 3 mins, 5 mins, 10 mins, 15 mins, 20 mins, 30 mins, 1 hour,
#     2 hours, 3 hours, 4 hours, 8 hours, 1 day, 1 week, 1 month

# the data duration is set to 8 hours (28800 seconds)

# can read/write a CSV OHLC file
#   if the file exists, the first file date/time becomes the inital request
#   so earlier historical data is requested and put at the front of the file

# uses Eastern Standard Time for data requests and writing date/time to CSV

from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
import os.path, time
import sys

def contract(contractTuple):
    newContract = Contract()
    newContract.m_symbol = contractTuple[0]
    newContract.m_secType = contractTuple[1]
    newContract.m_exchange = contractTuple[2]
    newContract.m_currency = contractTuple[3]
    newContract.m_expiry = contractTuple[4]
    newContract.m_strike = contractTuple[5]
    newContract.m_right = contractTuple[6]
    print 'Contract Parameters: [%s,%s,%s,%s,%s,%s,%s]' % contractTuple
    return newContract

# convert UTC to New York EST timezone
def ESTtime(msg):
    return time.gmtime(int(msg.date) - (5 - time.daylight)*3600)

def printData(msg):
    if int(msg.high) > 0:
        dataStr =  '%s,%s,%s,%s,%s,%s' % (time.strftime('%Y,%m,%d,%H,%M,%S',
                                                        ESTtime(msg)),
                                          msg.open,
                                          msg.high,
                                          msg.low,
                                          msg.close,
                                          msg.volume)
        print dataStr
        #if write2file: newRowData.append(dataStr+'\n')
    else:
		printData.finished = True

def watchAll(msg):
    print msg

if __name__ == "__main__":
    con = ibConnection()
    con.registerAll(watchAll)
    con.unregister(watchAll, message.historicalData)
    con.register(printData, message.historicalData)
    con.connect()
    time.sleep(1)
    symbol = sys.argv[1]
    duration = sys.argv[2]
    bar_length = sys.argv[3]
    contractTuple = (symbol, 'STK', 'SMART', 'USD', '', 0.0, '')

    endSecs = time.time()-(5-time.daylight)*60*60  # to NY EST via gmtime
    NYtime = time.gmtime(endSecs)

    # combined dateStr+timeStr format is 'YYYYMMDD hh:mm:ss TMZ'
    dateStr = time.strftime('%Y%m%d', NYtime)
    timeStr = time.strftime(' %H:%M:%S EST', NYtime)

    #barLength = '5 mins'  #  see top of file for accepted values

    newRowData = []

    printData.finished = False # true when historical data is done
    print 'End Date/Time String: [%s]' % (dateStr+timeStr)
	# dateStr + timeStr looks like this: [20140701 20:38:01 EST]

    # THIS IS WHERE THE MAGIC HAPPENS
    con.reqHistoricalData(0,
                          contract(contractTuple),
                          dateStr+timeStr, # last requested bar date/time
                          #'28800 S',  # quote duration, units: S,D,W,M,Y # 8 hours
                          #'7200 S',  # quote duration, units: S,D,W,M,Y # 2 hours
                          #'300 S',  # quote duration, units: S,D,W,M,Y # 2 hours
                          duration,  # quote duration, units: S,D,W,M,Y # 2 hours
                          #barLength,  # bar length
                          bar_length,  # bar length
                          #'0 mins',  # bar length
                          #'15 mins',  # bar length
                          'TRADES',  # what to show
                          #'BID_ASK',  # what to show
                          #'ASK',  # what to show
                          #'BID',  # what to show
						  #'HISTORICAL_VOLATILITY',
						  #'OPTION_IMPLIED_VOLATILITY',

						  #TRADES
						  #MIDPOINT
						  #BID
						  #ASK
						  #BID_ASK
						  #HISTORICAL_VOLATILITY
						  #OPTION_IMPLIED_VOLATILITY


                          0, 2 )
    countSecs = 0
    while not printData.finished and countSecs < 20: # wait up to 20 seconds
        time.sleep(1)
        countSecs += 1
    con.disconnect()
    print 'CSV format: year,month,day,hour,minute,second,open,high,low,close,volume'
