#!/usr/bin/python

import run_all
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/util')
import db

# SET GLOBALS


def meanstdv(x):
    from math import sqrt
    n, sum, mean, std = len(x), 0, 0, 0
    for a in x:
	sum = sum + a
    mean = sum / float(n)
    for a in x:
	std = std + (a - mean)**2
    std = sqrt(std / float(n-1))
    return sum, mean, std


def meanstdv_dict(x):
    from math import sqrt
    n, sum, mean, std = len(x), 0, 0, 0
    for a in x:
	sum = sum + x[a]
    mean = sum / float(n)
    for a in x:
	std = std + (x[a] - mean)**2
    std = sqrt(std / float(n-1))
    return sum, mean, std

#def main(amount, year,month, duration, fama_offset, min_alpha, min_sig, min_assets, max_assets):
def main(amount, year,month):
	value = {}
	date_range = []	
	sum, avg, std = 0, 0, 0
	conn = db.get_conn()
	cursor = db.get_conn()

	# Gather all dates in month
 	cursor.execute ("select distinct d.date from asset_value av, dates d where av.date_id = d.date_id and d.year = \'"+year+"\' and d.month_num = "+month+" and av.asset = 'AAPL' and av.volume != 0 order by av.date_id")
	rows = cursor.fetchall()
	for row in rows:
			date_range.append(row)

	for process_date in date_range:
		print process_date[0]
		print amount, str(process_date[0]), "4","30", ".0025", "2", "1", "20"
		value[process_date[0]] = run_all.main(amount, str(process_date[0]), "4", "30", ".0025", "2", "1", "20")
		print value[process_date[0]]

	try:
		sum, avg, std = meanstdv_dict(value)
	except:
		print "fail"
		print value
		
	print "Date = "+year+"-"+month+", Average Return = "+str(avg)+", Std dev = "+str(std)+", Return = "+str(sum)
	return(sum)
	cursor.close()
	conn.commit()



if __name__ == '__main__':
	amount = sys.argv[1]
	year = sys.argv[2]
	month = sys.argv[3]
	main(amount,year,month)

