#!/usr/bin/python

import run_month
import sys


def main(amount, year):
	value = []
	date_range = []	
	sum = 0
	for i in range(12):
		value.append(run_month.main(amount,str(year),str(i+1)))

	for i in value:
		sum = sum + int(i)

	print "Total return = "+str(sum)




if __name__ == '__main__':
	amount = sys.argv[1]
	year = sys.argv[2]
	main(amount,year)

