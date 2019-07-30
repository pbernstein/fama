#!/usr/bin/python

import sys
import os
import math
import time
from datetime import datetime
from dateutil import parser
import datetime as dt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

# SET GLOBALS

conn = db.get_conn()
cursor = conn.cursor()

# SET DEBUGGING LEVEL

#DETAIL = "I"  # INFO
#DETAIL = "D" # DETAIL (this actually prints everything)
#DETAIL = "P" # PERFORMANCE (only times)
DETAIL = "N" # This is a stub for don't print anything

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def printl(self, type):
	# I = Info, D = Debug
	# If DETAIL = I, then only print I
	# If DETAIL = D, then print I and D
	
	if DETAIL == "D":
		print self

	if DETAIL == "P":
		if type == "P":
			print self

	if DETAIL == "I":
		if type == "I":
			print self


def transposed(lists):
        if not lists: return []
        return map(lambda *row: list(row), *lists)


def gather_stocks(date,regression_output,min_alpha,min_sig,trade_type):
#	os.system("gunzip "+str(regression_output)+".gz")
        f = open(regression_output)
	min_open =  5
        assets = []
#	excluded_assets = []
	excluded_assets = ['CETV','RIMM','ARBA','ETFC']
        printl("Gathering Assets","P")
        t0=time.clock()

        cursor.execute ("SELECT date_id from dates where date = \""+str(date)+"\"")
        row = cursor.fetchone()
        date_id = str(row[0])

	duration = regression_output[find_nth(regression_output,"_",3)+1:find_nth(regression_output,"_",4)]

        for row in f:
		printl("gather_stocks row"+row,"D")
                columns = []
                for col in row.split(" "):
                        if (col.find('\n') != -1):
                                col = col[:col.find('\n')]
                        columns.append(col)
                if columns[0] != "mkt.Rf" and columns[0] != "smb" and columns[0] != "hml":
                        if trade_type == "buy":
                                if (round(float(columns[1]), 4) > min_alpha and round(float(columns[2]), 3) > min_sig):
					asset_name = columns[0]
					if asset_name.find("DATE.1") != -1:
						asset_name = "DATE"
					if asset_name.find("SMB.1") != -1:
						asset_name = "SMB"
					if asset_name.find("HML.1") != -1:
						asset_name = "HML"
		                        cursor.execute ("select av.exchange from asset_value av where av.asset = \""+asset_name+"\" limit 1")
       			                row = cursor.fetchone()
					try: 
	                       			exchange = row[0]
					except:
						print asset_name+" doesn't have an exchange"
						exchange = ""
					try:
						excluded_assets.index(asset_name)
						exclude = 1
					except:
						exclude = 0
					if exchange == "NASDAQ" and exclude == 0:
	                                 		assets.append(columns)
                                assets.sort(key=lambda x: float(x[1]), reverse=True)
                        else:
                                if (round(float(columns[1]), 3) < (min_alpha * -1) and round(float(columns[2]), 3) > min_sig): 
					asset_name = columns[0]
					
					if asset_name.find("DATE.1") != -1:
						asset_name = "DATE"

		                        cursor.execute ("select av.exchange from asset_value av where av.asset = \""+asset_name+"\" limit 1")
       			                row = cursor.fetchone()
					try:
 	                      			exchange = row[0]
					except:
						print asset_name+" has no exchange"
						exchange = ""
					try:
						excluded_assets.index(asset_name)
						exclude = 1
					except:
						exclude = 0
					if exchange == "NASDAQ" and exclude == 0:	
       	                                        	assets.append(columns)
        			assets.sort(key=lambda x: float(x[1]), reverse=False)
        printl("Elapsed time: "+str(time.clock() - t0),"P")
        return assets 


def calculate_value(amount, duration, fama_offset, min_alpha, min_sig, min_assets, max_assets, process_date, buy_assets, sell_assets):

	"""
	First i need to understand what allocation to give to each asset
 		I need to create as many even lots and mixed lots as possible 
		Then redistribute the amount accross each of those assets
	Then i will call port value, which i should rename to asset_return,
		Which will give me the return on that stock

	"""

	#print " calculate value amount :" +str(amount)	
        cv_conn = db.get_conn()
        cv_cursor = cv_conn.cursor()
	full_asset_list = []


	cursor.execute ("SELECT date_id from dates where date = \""+str(process_date)+"\"")
        row = cursor.fetchall()
        date_id = row[0][0]
	"""
	print "buy_assets", str(buy_assets)
	print "sell_assets", str(sell_assets)
	"""

	# Ensure buy assets and sell portfolios meet the max/min criteria
	trimmed_buy_assets = []
	trimmed_sell_assets = []
	for assets in buy_assets, sell_assets:
       	 	asset_names = []
		trade_type = ""
		try:
			buy_assets.index(assets[0])
			trade_type = "BUY"
		except:
			trade_type = "SELL"
        	if  len(assets) < max_assets:
  	         num_assets = len(assets)
       	 	else:
       	         num_assets = max_assets
	        for i in range(num_assets):
			if trade_type == "BUY":
	       	         trimmed_buy_assets.append(assets[i][0])
			else:
	       	         trimmed_sell_assets.append(assets[i][0])
		if trade_type == "BUY":
			tmp = 1
				
	#  Now, fix the lot sizes
	
	total_assets = len(trimmed_buy_assets) + len(trimmed_sell_assets)
	try:
		ration = int(amount) / int(total_assets)
	except:
		ration = 0

	"""
	print "total assets = " +str(total_assets)
	print "amount = " +str(amount)
	print "ration = " +str(ration)
	"""

	# This will condense trimmed_buy_assets and trimmed_sell assets into one list
	for asset_names in trimmed_buy_assets, trimmed_sell_assets:
		try:
			trimmed_buy_assets.index(asset_names[0])
			trade_type = "BUY"
		except:
			trade_type = "SELL"
		asset = ""
		for asset in asset_names:
			cursor.execute ("select av.close from asset_value av where av.date_id < "+str(date_id)+" and av.asset = \""+asset+"\" order by av.date_id desc limit 1")
	                row = cursor.fetchone()
			close = row[0]	

			num_shares =  math.floor(float(ration) / float(close))

			floor_share = 35
			if num_shares < floor_share:
				num_shares = 0
			if num_shares > floor_share and num_shares < 100:
				num_shares = 100
			if num_shares >= 100:
				full_asset_list.append([asset, close, num_shares, close * num_shares, trade_type])

	#  Lot sizes for assets in full_asset_list  have been corrected!!
	#  Now I need to reallocate the amount over the assets with even and mixed lot sizes

	# Ensure I still have enough assets to qualify as diversified
	"""
	total_investing_assets = len(buy_assets) + len(sell_assets)
	if total_investing_assets < (int(max_assets) / 2):
		full_asset_list = []
	"""

#	print "initial full asset list "+str(full_asset_list)
	total_alloc = 0
	total_assets = 0
	for asset_details in full_asset_list:
			total_alloc = total_alloc + asset_details[3]
			total_assets = total_assets + 1



	excess_amount = 0
	if total_alloc < int(amount):
		excess_amount = amount - total_alloc

	"""  INVESTING EXCESS AMOUNT
	
	if excess_amount > 0:
		asset_count = len(full_asset_list)	
		for asset_details in full_asset_list:
			# New num_shares 
			asset_details[2] = num_shares + math.floor((excess_amount/asset_count)/asset_details[1])
		#New Allocation
			asset_details[3] = asset_details[1] * asset_details[2]
	
	#INVESTING EXCESS AMOUNT END
	"""


	# NOW! I can finaly predict the return of each asset			

#	print "fixed full asset list "+str(full_asset_list)
	profit = 0
	asset_return = 0
	for asset_details in full_asset_list:
			asset_return = portfolio_value(asset_details[2], amount, duration, fama_offset, min_alpha, min_sig, min_assets, max_assets, process_date, date_id, asset_details[0], asset_details[4])
			profit = profit + asset_return
#			print "asset: "+str(asset_details[0])+" trade: "+str(asset_details[4])+ " shares: "+str(asset_details[2])+" allocation "+str(asset_details[3])+" profit: "+str(asset_return)
	if profit == 0:
		try:
	                cv_cursor.execute ("INSERT INTO daily_returns (`date_id`, `amount`, `allocation`, `duration`, `fama_offset`, `min_alpha`,`min_sig`, `min_assets`, `max_assets`,   `profit`) VALUES ("+",".join(map(str, [date_id,amount,0,duration,fama_offset,min_alpha,min_sig,min_assets,max_assets,profit]))+")")
        		cv_conn.commit()
#	                print "INSERT INTO daily_returns (`date_id`, `allocation`, `duration`, `fama_offset`, `min_alpha`,`min_sig`, `min_assets`, `max_assets`,   `profit`) VALUES ("+",".join(map(str, [date_id,amount,duration,fama_offset,min_alpha,min_sig,min_assets,max_assets,profit]))+")"
		except:
			tmp = 1
#			print "cv insert failed"

        cv_cursor.close()
	cv_conn.commit()
        cv_conn.close()
	return(profit)

def export_data(extract_output,process_date, duration, fama_offset):
        printl("export data process_date = "+str(process_date),"D")
#	if not os.path.exists(str(extract_output)+".gz"):
	if not os.path.exists(extract_output):
        	f_analysis = open(extract_output, 'w')
        	data_for_analysis = build_data(process_date, duration, fama_offset)
        	if data_for_analysis == 0:
                	print "There is no market data available for this day: "+process_date
	                return(1)

	        for row in data_for_analysis:
       	        	printl("data_for_analysis "+str(row),"D")
 	      	        f_analysis.write(row)
       	 	f_analysis.close()
#		os.system("gzip "+str(extract_output))
        return(0)


def run_regression(extract_output, regression_output):
        printl("Running Regression","P")
        t0=time.clock()
#        path = os.getcwd()
	duration = regression_output[find_nth(regression_output,"_",3)+1:find_nth(regression_output,"_",4)]
	tmp_file = regression_output[find_nth(regression_output,"/",6)+1:]
#	print "tmp_file = ", str(tmp_file)
	if not os.path.exists(regression_output):
        	try:
			# All this copying around is done because R eats "-" 
			# and turns it into a ".", which
			# is awful because "." exists in other asset names. 
			# This approach seemed the most contained 

			os.system("rm /tmp/temp_extract") 
#			os.system("gunzip "+str(extract_output)+".gz")
			os.system("head -1 "+extract_output+" | sed 's/-/_/g' > /tmp/temp_extract")
			os.system("sed '1d' "+extract_output+" >> /tmp/temp_extract")
			regression_command = "/home/peter/work/analysis/run_regression.ksh /tmp/temp_extract "+str(regression_output)
        	       	os.system(regression_command)
			os.system("rm /tmp/cleaned_regression")
			os.system("cat "+regression_output+" | sed 's/_/-/g' > /tmp/cleaned_regression")
			os.system("cp /tmp/cleaned_regression "+regression_output)
#			os.system("gzip "+str(extract_output))
#			os.system("gzip "+str(regression_output))
	        except:
			print "no regression dataset"
       	        	return(1)
        printl("Elapsed time: "+str(time.clock() - t0),"P")
        return(0)
	

def build_perm_data(permutations, fa):
#	permutations = [[[90,30,0,0,1],[90,60,0,0,1] .....],[234,-123,123,123,123, ...],[date1, date2, date3 ... ],[date_id1, date_id2, date_id3 ...]
# 	Returns:
#	[[[date1, [90,30,0,0,1], 234, mrkt_rf, smb, hml],[ ... ] ]
	header = []
	permutation_list = []
	profit_list = []
	date_list = []
	date_id_list = []



	for i  in permutations:
		permutation_list.append("A".join(map(str,i[0]))) # JUST REPLACED THE NESTED LISTS WITH STRINGS
		profit_buffer = []
		profit_list.append(i[1])
				
			
	for i in permutations[0][2]:
		date_list.append(i)
	for i in permutations[0][3]:
		date_id_list.append(i)

	fama_offset = fa
	fama_date_id_list = []
	fama_date_list = []
	for i in date_id_list:
	        cursor.execute("select f.date_id, (select dsc.date from dates dsc where dsc.date_id = f.date_id) as famadate from dates d, fama f, asset_value av where av.date_id = d.date_id and av.asset = 'AAPL' and av.volume > 0 and d.date_id < \'"+str(i)+"\' and f.date_id = (select csf.date_id from fama csf where csf.date_id <= (d.date_id - "+str(fama_offset)+")  and  (select csd.day_of_week from dates csd where csd.date_id = csf.date_id) = d.day_of_week order by csf.date_id desc limit 1) order by d.date_id desc limit 1")
        	row = cursor.fetchone()
		fama_date_id_list.append(int(row[0]))
		fama_date_list.append(row[1].strftime('%Y-%m-%d'))

	data_buffer = []
	profits_transposed = transposed(profit_list)


	t0=""


	header.append('date')
	header=header + permutation_list + ['mkt-rf'] + ['smb'] + ['hml'] 
	data_buffer.append(header)
	for i in range(len(date_list)):
		profit_buffer = []
        	cursor.execute("select mrkt_rf, smb, hml from fama where date_id = "+str(fama_date_id_list[i]))
	        fama_payload = cursor.fetchone()
		data_buffer.append([date_list[i],",".join(map(str,profits_transposed[i])), fama_payload[0], fama_payload[1], fama_payload[2]])
	
	data = ""
	for i in range(len(data_buffer)):
        	data =  data + ",".join(map(str,data_buffer[i])) + "\n"

#	print "data ", str(data)
	return data

def build_data(end_date,duration,fama_offset):
	duration = str(duration)
	fama_offset = str(fama_offset)
	header = []
	asset_buffer = []
	asset_name_list = []
	asset_prepped = []
	date_range = []
	data = ""
	t0=""

	# First, figure out ALL The dates
	# date_range = [ [ asset_date_id, asset_date, fama_date_id, fama_date],[asset_date_id, asset_date, fama_date_id, fama_date],etc.. ]

	printl("Running date query","P")
	t0=time.clock()

# 	Does NOT care about day of week
#	cursor.execute("select d.date_id, d.date, f.date_id, (select dsc.date from dates dsc where dsc.date_id = f.date_id) as famadate from dates d, fama f, asset_value av where av.date_id = d.date_id and av.asset = 'AAPL' and av.volume > 0 and d.date < \'"+str(end_date)+"\' and f.date_id = (select csf.date_id from fama csf where csf.date_id <= (d.date_id - 60) order by csf.date_id desc limit 1) order by d.date_id desc limit "+duration)


#	Does cares about day of week
#	Only uses dates where AAPL has a volume > 10000 (accounts for weekends and holidays)
#	print end_date
	month_day = end_date[end_date.rindex("-")+1:]
	month_num = end_date[end_date.index("-")+1:end_date.rindex("-")]
	year = end_date[0:end_date.index("-")]

	print "select date_id from dates where month_day <= "+str(month_day)+" and month_num = "+str(month_num)+" and year = ("+str(year)+" - "+str(duration)+") order by date desc limit 1"
	cursor.execute("select date_id from dates where month_day <= "+str(month_day)+" and month_num = "+str(month_num)+" and year = ("+str(year)+" - "+str(duration)+") order by date desc limit 1")
	min_date_id = int(cursor.fetchone()[0])
#	print min_date_id	

	
	print "select d.date_id, d.date, f.date_id, (select dsc.date from dates dsc where dsc.date_id = f.date_id) as famadate from dates d, fama f, asset_value av where av.date_id = d.date_id and av.asset = 'AAPL' and av.volume > 10000  and av.open > 5 and d.date < \'"+str(end_date)+"\' and f.date_id = (select csf.date_id from fama csf where csf.date_id <= (d.date_id - "+str(fama_offset)+")  and  (select csd.day_of_week from dates csd where csd.date_id = csf.date_id) = d.day_of_week order by csf.date_id desc limit 1) and d.date_id >= "+str(min_date_id)
	cursor.execute("select d.date_id, d.date, f.date_id, (select dsc.date from dates dsc where dsc.date_id = f.date_id) as famadate from dates d, fama f, asset_value av where av.date_id = d.date_id and av.asset = 'AAPL' and av.volume > 10000  and av.open > 5 and d.date < \'"+str(end_date)+"\' and f.date_id = (select csf.date_id from fama csf where csf.date_id <= (d.date_id - "+str(fama_offset)+")  and  (select csd.day_of_week from dates csd where csd.date_id = csf.date_id) = d.day_of_week order by csf.date_id desc limit 1) and d.date_id >= "+str(min_date_id))



    	printl("Elapsed time: "+str(time.clock() - t0),"P") 

        rows = cursor.fetchall()
        for row in rows:
		date_buffer = []
                date_buffer.append(int(row[0]))
                date_buffer.append(row[1].strftime('%Y-%m-%d'))
                date_buffer.append(int(row[2]))
                date_buffer.append(row[3].strftime('%Y-%m-%d'))
		date_range.append(date_buffer)

	date_range.sort(reverse=True)
        printl("build data date range "+str(date_range),"D")
	
	fama_date_ids = ""
	asset_date_ids = ""
	for i in date_range:
		asset_date_ids = asset_date_ids + str(i[0])+","
	#for i in date_range:
		fama_date_ids = fama_date_ids + str(i[2])+","

	asset_date_ids = asset_date_ids[:-1]
	fama_date_ids = fama_date_ids[:-1]

        printl("asset_Date_id "+str(asset_date_ids),"D")
        printl("fama_Date_id "+str(fama_date_ids),"D")


	# Start Asset Buffer
	for date in date_range:
		temp_list = []
		temp_list.append(date[1])
		asset_buffer.append(temp_list)

	# Asset name list
	printl("Running asset name query","P")
	t0=time.clock()



	#print " select count(*) from asset_value where date_id in ("+str(asset_date_ids)+") and volume > 10000 and open > 5 and asset = \'AAPL\' group by asset"
	cursor.execute (" select count(*) from asset_value where date_id in ("+str(asset_date_ids)+") and volume > 10000 and open > 5 and asset = \'AAPL\' group by asset") 
	new_duration = str(int(cursor.fetchone()[0]))
	#print "new duration = "+str(new_duration)
	
	"""
	###  ONLY use assets that have a 
	 trading volume of 10000 or higher and a   ->  I want to be able to get in and get out
	 open price of 5 dollars or higher         ->  Too low an open = too much volatility
	 for the entire dataset of the regression
	"""

	"""
	print " select asset from asset_value where date_id in ("+str(asset_date_ids)+") and volume > 10000 and open > 5 group by asset having count(asset) = "+str(new_duration)+" order by asset"
	print "date ids: "+str(asset_date_ids)
	"""

	#cursor.execute (" select asset from asset_value where date_id in ("+str(asset_date_ids)+") and volume > 10000 and open > 5 group by asset having count(asset) = "+duration+" order by asset") 
	cursor.execute (" select asset from asset_value where date_id in ("+str(asset_date_ids)+") and volume > 10000 and open > 5 group by asset having count(asset) = "+str(new_duration)+" order by asset") 

    	printl("Elapsed time: "+str(time.clock() - t0),"P") 
	asset_name_list = transposed(cursor.fetchall())[0]
 

	printl("Running data build for loop","P")
	t0=time.clock()
	for i in range(len(date_range)):
		cursor.execute("select percent_change from asset_value where asset in ("+"'"+"','".join(asset_name_list)+"'"+") and date_id = "+str(date_range[i][0])+" order by asset")
		asset_payload = cursor.fetchall()
		asset_payload = transposed(asset_payload)
		asset_payload = transposed(asset_payload)
		for pc in asset_payload:
			asset_buffer[i].append(pc[0])

        	cursor.execute("select mrkt_rf, smb, hml from fama where date_id = "+str(date_range[i][2]))
	        fama_payload = cursor.fetchall()
		fama_payload = transposed(fama_payload)
		fama_payload = transposed(fama_payload)
		asset_buffer[i].append(fama_payload[0][0])
		asset_buffer[i].append(fama_payload[0][1])
		asset_buffer[i].append(fama_payload[0][2])
	
    	printl("Elapsed time: "+str(time.clock() - t0),"P") 


	header.append('date')
	header=header + asset_name_list + ['mkt-rf'] + ['smb'] + ['hml'] 

	asset_prepped.append(header)
	for row in asset_buffer:		
		asset_prepped.append(row)

	asset_prepped_len = len(asset_prepped[0])
	for row in asset_prepped:
		if len(row) != asset_prepped_len:
			print "len(row) = "+str(len(row))
			print "Asset Data is Boned!!!!"  
			print asset_prepped
			exit(0)


	for i in range(len(asset_prepped)):
        	data =  data + ",".join(map(str,asset_prepped[i])) + "\n"

	return data



def portfolio_value(num_shares, amount, duration, fama_offset, min_alpha, min_sig, min_assets, max_assets, date, date_id, asset, trade_type):

        pf_conn = db.get_conn()
        pf_cursor = pf_conn.cursor()

	FPT = .01 # .005 fee per trade, set by IB
	if num_shares > 200:
		FEE = FPT * num_shares
	else:
		FEE = 2

	sum = 0
	delimiter=","
	if trade_type == "BUY":
		transaction = 1
	else:	
		transaction = 0


        printl("Portfolio value","P")
        t0=time.clock()
	allocation = 0

	cache = ""
	cache_print = 1
	cache = str(num_shares) +" "+ str(date)+" " + trade_type + " " + str(num_shares) + " |"
#	print str(asset) +" "+ str(num_shares) +" "+ str(date)+" " + trade_type + " " + str(num_shares) 
	cache =  cache +str(asset)+" "+str(trade_type.upper())+" "+str(num_shares)+";"

	pf_cursor.execute ("select av.open, av.close, av.high, av.low from asset_value av where av.date_id = "+str(date_id)+" and av.asset = \""+asset+"\"")
	rows = pf_cursor.fetchall()
	if len(rows) != 0:
		for row in rows: 
				
			if row[0] == 0 or row[1] == 0:
				print "Chosen asset has an open/close value of 0, probably bad data. Date: "+str(date)+" Asset: "+str(asset)+" open: "+str(row[0])+" close: "+str(row[1])
				sys.exit(1)	
		        else:
				open = row[0]
				close = row[1]
				high = row[2]
				low = row[3]
				allocation = int(num_shares) * int(open)
				if trade_type == "BUY":		
					profit = (num_shares * (close - open)) - FEE 
				else:
					profit = (num_shares * (open - close)) - FEE
	else:		
#		print "Chosen asset has no row. Bad data? Date: "+str(date)+" Date id: "+str(date_id)+" Asset: "+str(asset)
#		print "Chosen asset has no row. Bad data? Date: "+str(date)+" Date id: "+str(date_id)+" Asset: "+str(asset)Q
		print
		print "./manually_place_mktopg.py "+str(asset), str(trade_type.upper()) ,str(int(num_shares))+"; sleep 2; ./manually_place_mktcls.py", str(asset), 
		if str(trade_type.upper()) == "BUY":
			print "SELL",
		else:
			print "BUY",
		print str(int(num_shares))+"; sleep 2; "
		
		profit = 0
		allocation = 0
	try:
#		print "Attempting to load returns"
		pf_cursor.execute ("INSERT INTO daily_returns (`date_id`, `amount`, `allocation`, `duration`, `fama_offset`, `min_alpha`,`min_sig`, `min_assets`, `max_assets`, `asset`, `trade`, `buy`, `sell`, `profit`) VALUES ("+",".join(map(str, [date_id,amount,allocation,duration,fama_offset,min_alpha,min_sig,min_assets,max_assets,str("\""+asset+"\""),transaction,row[0],row[1],profit]))+")")
        	pf_conn.commit()
        except:
		tmp = 1



	cache_print = 0

	if cache_print != 0:
		print cache[:-1] + "|"

        printl("Elapsed time: "+str(time.clock() - t0),"P")
        pf_cursor.close()


	return(profit)


def main(amount, date, trade_type, assets):
	asset_list = assets.split(" ")
	amount_int = int(amount)
	print "return = "+str(portfolio_value(amount_int, date, asset_list, trade_type))
	

if __name__ == '__main__':
        amount = sys.argv[1]
        process_date = sys.argv[2]
        trade_type = sys.argv[3]
        assets = sys.argv[4]
        main(amount, process_date, trade_type, assets)

	


