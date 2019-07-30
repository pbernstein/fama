#!/usr/bin/python

import sys
import os
import investments as inv
import send_email
	



def day_return(amount, process_date, duration,fama_offset, min_alpha,min_sig, min_assets, max_assets, load, trade = "buy"):
	min_alpha = float(min_alpha)
	min_sig = float(min_sig)
	min_assets = int(min_assets)
	max_assets = int(max_assets)
	buy_assets = []
	sell_assets = [] 
	home_path = os.getenv("HOME")


	
	extract_output = "/media/data/investments/data/staging/automated_daily_analysis_"+str(process_date)+"_"+str(duration)+"_"+str(fama_offset)+".dat"
	regression_output = "/media/data/investments/data/staging/regression_results_"+str(process_date)+"_"+str(duration)+"_"+str(fama_offset)+".dat"

	if inv.export_data(extract_output, process_date, duration, fama_offset) == 1:
		print "No data to export!"
		return(1)

	if inv.run_regression(extract_output, regression_output) == 1:
		print "Regression Fail!"
		return(1)

	##	
	# Gather Assets
	## 	
	used_alpha = min_alpha

	while ((len(buy_assets) + len(sell_assets)) < min_assets or len(buy_assets) == 0 or len(sell_assets) == 0) and used_alpha > .001:
		buy_assets = inv.gather_stocks(process_date,regression_output,used_alpha,min_sig,"buy")	
		sell_assets = inv.gather_stocks(process_date, regression_output,used_alpha,min_sig,"sell")	
		used_alpha = float(used_alpha) - float(.0001)


	if used_alpha == 1:
		buy_assets = []
		sell_assets = []
	profit =  0


	profit = inv.calculate_value(int(amount), duration, fama_offset, min_alpha, min_sig, min_assets, max_assets, process_date, buy_assets, sell_assets) 
	return (buy_assets, sell_assets, profit)

