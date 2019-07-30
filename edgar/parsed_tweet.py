#!/usr/bin/python

import os
import sys
import twitter
import locale
from datetime import datetime


def compare_tweet(symbol, attribute, value,pre_value):
	my_auth = twitter.OAuth('','','','')
	twit = twitter.Twitter(auth=my_auth)

	# auth=OAuth(token, token_key, con_secret, con_secret_key))
	#if delta > 0:
	#	twit.statuses.update(status=name.replace("_"," ")+" "+exchange+":"+symbol+" posts revenue of "+str(revenue)+",)

	flag = "/tmp/"+str(datetime.now()).split(" ")[0]+"_"+attribute+"_"+symbol+".compare_tweet"
	locale.setlocale( locale.LC_ALL, '' )
	dollar_value = locale.currency( int(value), grouping=True )
	percent = int(float(pre_value)/float(value) * 100)

	if float(value) > float(pre_value):
	    msg = "$"+symbol +" posts "+dollar_value +" in "+attribute+", a gain of "+str(percent)+" percent from last quarter"
	else:
	    msg = "$"+symbol +" posts "+dollar_value +" in "+attribute+", a drop of "+str(percent)+" percent from last quarter"
	#if not os.path.exists(flag):
	#if 1 == 1:
	if value != pre_value:

		print "Parsed Tweeting: "+msg
		#twit.statuses.update(status=msg)
		#print symbol +" posts "+dollar_value +" in "+attribute
		o = open(flag,'w')
		o.close()
		return 1
	return 0

def tweet(symbol, attribute, value):
	my_auth = twitter.OAuth('','','','')
	twit = twitter.Twitter(auth=my_auth)

	# auth=OAuth(token, token_key, con_secret, con_secret_key))
	#if delta > 0:
	#	twit.statuses.update(status=name.replace("_"," ")+" "+exchange+":"+symbol+" posts revenue of "+str(revenue)+",)

	flag = "/tmp/"+str(datetime.now()).split(" ")[0]+"_"+attribute+"_"+symbol+".tweet"
	locale.setlocale( locale.LC_ALL, '' )
	dollar_value = locale.currency( int(value), grouping=True )

	msg = "$"+symbol +" posts "+dollar_value +" in "+attribute
	#if not os.path.exists(flag):
	if 1 == 1:

		print "Parsed Tweeting: "+msg
		twit.statuses.update(status=msg)
		print "$"+symbol +" posts "+dollar_value +" in "+attribute
		o = open(flag,'w')
		o.close()
		return 1
	return 0


if __name__ == '__main__':
	symbol = sys.argv[1]
	attribute = sys.argv[2]
	value = sys.argv[3]
	prev_value = sys.argv[4]
	#tweet(symbol, attribute, value)
	compare_tweet(symbol, attribute, value,prev_value)

