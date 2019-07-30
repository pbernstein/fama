#!/usr/bin/python

import os
import glob

from time import strptime

from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
import os.path, time
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

progress = 0
eh_sk = 0
bar_length = "5 min"

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
#    return time.gmtime(int(msg.date))


# convert UTC to CST timezone
def CSTtime(msg):
    return time.gmtime(int(msg.date) - (6 - time.daylight)*3600)

def printData(msg):
    if int(msg.high) > 0:
		dataStr =  '%s,%s,%s,%s,%s,%s' % (time.strftime('%Y,%m,%d,%H,%M,%S',
                                                        CSTtime(msg)),
                                          msg.open,
                                          msg.high,
                                          msg.low,
                                          msg.close,
                                          msg.volume)
		print dataStr



		# inherit global eh_sk and bar_length

		instant = time.strftime('%Y-%m-%d %H:%M:%S',  CSTtime(msg))

		o = str(msg.open)
		h = str(msg.high)
		l = str(msg.low)
		c = str(msg.close)
		v = str(msg.volume)
		cursor.execute("insert into histprice (`eh_sk`,`bar_length`,`instant`,`open`,`high`,`low`,`close`,`volume`) values ("+str(eh_sk)+",'"+str(bar_length)+"','"+str(instant)+"',"+o+","+h+","+l+","+c+","+v+")")
		conn.commit()

        printData.finished = True

def watchAll(msg):
    print msg


def populate_price():
		# open the
		con = ibConnection()
		con.registerAll(watchAll)
		con.unregister(watchAll, message.historicalData)
		con.register(printData, message.historicalData)
		con.connect()
		time.sleep(1)



		cursor.execute("select e.eh_sk, e.cik, s.symbol, e.form,  YEAR(e.insert_ts) as year, MONTH(e.insert_ts) as month, DAY(e.insert_ts) as day, HOUR(e.insert_ts) as hour, MINUTE(e.insert_ts) as minute, c.industry_id from extract_history e, company c, symbol s where e.cik = c.cik and e.status = 'S' and e.cik = s.cik and e.date_id > s.start_date_id and e.date_id <= s.end_date_id and e.date_id > 8767  and hour(e.insert_ts) < 15 and cast(e.insert_ts as time) > cast('08:30:00' as time)  and eh_sk = 1359157 group by cik, year, month, day, hour, minute order by e.insert_ts limit 20")


        cursor.execute("select * from ins_map where eh_sk not in (select eh_sk from filing_price) and date_id > 8963")


		rows = cursor.fetchall()
		for row in rows:
				print row
				global eh_sk
				eh_sk = row[0]
				cik = row[1]
				symbol = row[2]
				form = row[3]
				year = row[4]
				month = row[5]
				day = row[6]
				hour = row[7]
				minute = row[8]
				industry = row[9]


				# THIS TIMESTAMP IS IN CENTRAL, WHEN I LOADED THE RECORD DURING THE FILING EXTRACT, INSERT_TS WAS A 'CURRENT TIMESTAMP'
				# I NEED TO CONVERT THIS TO EST
						# add 1  to hour
				# I WANT 1 HOUR BEFORE AND 1 AFTER
						# subtract 1 hour
				# SET DURATION TO 2 HOURS
						# 2 hours * 60 * 60 = 7200
				hour = str(int(hour) + 1)



				contractTuple = (symbol, 'STK', 'SMART', 'USD', '', 0.0, '')

				requestTime = str(year)+str(month).zfill(2)+str(day).zfill(2)+" 16:01:01 EST"
				print str(year)+str(month).zfill(2)+str(day).zfill(2)+" "+str(int(hour) - 1).zfill(2)+":"+str(minute).zfill(2)+":01 EST"

				# set duration
				#duration = "7200"
				#duration = "28800"
				duration = '60'


				bar_length = '5 mins'  #  see top of file for accepted values
				bar_length = '15 mins'  #  see top of file for accepted values
				bar_length = '1 min'  #  see top of file for accepted values
				newRowData = []
				printData.finished = False # true when historical data is done
				# dateStr + timeStr looks like this: [20140701 20:38:01 EST]


				#price, neg1, neg1min, neg1max, pos1, pos1min, pos1max = get_price(con, contractTuple, duration, requestTime, barLength)
				#price, neg4, neg4min, neg4max, pos4, pos4min, pos4max = get_price(con, contractTuple, duration, requestTime, barLength)
				con.reqHistoricalData(0,
								  contract(contractTuple),
								  requestTime, # last requested bar date/time
								  #'28800 S',  # quote duration, units: S,D,W,M,Y # 8 hours
								  #duration+' S',  # quote duration, units: S,D,W,M,Y # 2 hours is 7200, 4 hours is 14400
								  duration,  # quote duration, units: S,D,W,M,Y # 2 hours is 7200, 4 hours is 14400
								  #barLength,  # bar length
								  bar_length,  # bar length
								  #'15 mins',  # bar length
								  'TRADES',  # what to show
								  #'BID_ASK',  # what to show
								  #'ASK',  # what to show
								  #'BID',  # what to show
								  #'HISTORICAL_VOLATILITY',
								  #'OPTION_IMPLIED_VOLATILITY',
                          0, 2 )

			    time.sleep(1)

		con.disconnect()








conn = db.get_conn()
cursor = conn.cursor()
if __name__ == "__main__":
	populate_price()

cursor.close()
conn.commit()
conn.close()


