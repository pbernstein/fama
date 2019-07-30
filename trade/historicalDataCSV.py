#!/usr/bin/env python
# -*- coding: utf-8 -*-

# uses 12 hours ago as the end date for the inital data request
# and works it's way backwards in time: if it finds an existing csv file
# with the same name, the first line is used to get the end date
# and new data is put at the front

from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
import os.path, time
from time import sleep
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

def watchAll(msg):
    print msg

def printData(msg):
    if int(msg.high) > 0:
        dataStr =  '%s,%s,%s,%s,%s,%s' % (time.strftime('%Y,%m,%d,%H,%M,%S', time.localtime(int(msg.date))),
                            msg.open, msg.high, msg.low, msg.close, msg.volume)
        print dataStr
        if write2file: newDataList.append(dataStr+'\n')
    else:
        con.meFinished = True

if __name__ == "__main__":
    action = sys.argv[1]	
    symbol = sys.argv[2]	
    date = sys.argv[3] 
    if action  == "0":
	action = "SELL"
    else:
        action = "BUY"
#BUY_CMED_STK_20110609_1min.csv
    fn = "/home/ubuntu/work/tick/"+action+"_"+symbol+"_STK_"+date+"_1min.csv"
    print "looking for "+fn
    if os.path.isfile(fn):
	print "Found "+fn
	print "Exiting!"			
	sys.exit(0)
	
    con = ibConnection()
    con.registerAll(watchAll)
    con.unregister(watchAll, message.HistoricalData)
    con.register(printData, message.HistoricalData)
    con.connect()
    time.sleep(1)
#    contractTuple = ('QQQQ', 'STK', 'SMART', 'USD', '', 0.0, '')
#    contractTuple = (str(symbol), 'STK', 'SMART', 'USD', '', 0.0, '')
    contractTuple = (str(symbol), 'STK', 'SMART', 'USD', '', 0.0, '')
    #contractTuple = ('QQQQ', 'OPT', 'SMART', 'USD', '20070921', 45.0, 'CALL')
    #contractTuple = ('ES', 'FUT', 'GLOBEX', 'USD', '200802', 0.0, '')
    #contractTuple = ('ES', 'FOP', 'GLOBEX', 'USD', '20070920', 1460.0, 'CALL')
    #contractTuple = ('EUR', 'CASH', 'IDEALPRO', 'USD', '', 0.0, '')  # doesn't work!
    
    # combined dateStr+timeStr format is 'YYYYMMDD hh:mm:ss TMZ'
    #yesterdaySecs = time.time() - 12*60*60 # first default end date is 12 hours ago
    yesterdaySecs = time.time() - 12*60*60 # first default end date is 12 hours ago
    # dateStr is used in the default filename, timeStr is not
#    dateStr = time.strftime('%Y%m%d', time.localtime(yesterdaySecs))
    dateStr = date			
    timeStr = time.strftime(' %H:%M:%S EST', time.localtime(yesterdaySecs))
    
    # change write2file to True to actually write data to: fileName
    write2file = True
    if write2file:
        extraStr = '_1min' # use this to add the bar length, etc. to the name
        defaultFilename = action+'_'+contractTuple[0]+'_'+contractTuple[1]+'_'+dateStr+extraStr+'.csv'
        fileName = "/home/ubuntu/work/tick/"+defaultFilename # change this line to use your own filename
        if os.path.isfile(fileName): # found a previous version
            file = open(fileName, 'r')
            fileList = file.readlines()
            file.close()
            if len(fileList) > 1:
                fileList.pop(0)
                firstData = fileList[0] # get the new end date and time from the first data line of the file
                timeStr = ' %s:%s:%s EST' % (firstData[11:13],firstData[14:16],firstData[17:19])
                dateStr = '%s%s%s' % (firstData[0:4],firstData[5:7],firstData[8:10])
            else: firstData = 'firstData'
            time.sleep(2)
        else:
            fileList = [] # and use yesterday for the end date
            firstData = 'firstData'
        file = open(fileName, 'w')
    newDataList = []
    con.meFinished = False # so that it can know when it is done
    print 'End Date String: [%s]' % (dateStr+timeStr)
#    con.reqHistoricalData(0, contract(contractTuple), dateStr+timeStr, # end date
#                                                '3600 S',  # duration
#                                                '15 mins',  # bar length
#                                                'TRADES',  # what to show
#                                                0, 2 )

    dateStr = time.strftime('%Y%m%d', time.localtime(yesterdaySecs))
    print "dateStr "+str(dateStr) 		
    print "timeStr "+str(timeStr) 		
    timeStr = time.strftime(' %H:%M:%S EST', time.localtime(yesterdaySecs))
    dateStr = date			
    timeStr = " 18:00:00 EST"	
    print "dateStr "+str(dateStr) 		
    print "timeStr "+str(timeStr) 		

    con.reqHistoricalData(0, contract(contractTuple), dateStr+timeStr, # end date
#                                                '3600 S',  # duration, 1 HR
                                                '1 D',  # duration, 8 HR
                                                '1 min',  # bar length
                                                'TRADES',  # what to show
                                                0, 2 )


    countSecs = 0
    while not con.meFinished and countSecs < 20: # give up after 20 seconds
        time.sleep(1)
        countSecs += 1
    con.disconnect()
    	
    if write2file:
        newDataList.extend(fileList)
        if newDataList.count(firstData) > 1: # for daily bars the end date data gets repeated
            newDataList.remove(firstData)
            print 'Duplicate line removed'
        file.write('Year,Month,Day,Hour,Minute,Second,Open,High,Low,Close,Volume\n')
        file.writelines(newDataList)
        file.close()
        time.sleep(2)
        print 'CSV format: year,month,day,hour,minute,second,open,high,low,close,volume'
        print 'CSV data prepended to file: ', fileName
    else: print 'Finished'
    sleep(15)
