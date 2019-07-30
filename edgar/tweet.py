#!/usr/bin/python

import os
import sys
import twitter


def tweet(name, exchange, symbol, form):

        # add your values 
        api = twitter.Api(consumer_key='', consumer_secret='', access_token_key='', access_token_secret='')
        api.PostUpdate(name.replace("_"," ")+" $"+symbol+" "+form+" now available")
	
	
	o = open("/tmp/"+symbol+"_"+form+".tweet","w")
	o.close()


if __name__ == '__main__':
	name = sys.argv[1]
	exchange = sys.argv[2]
	symbol = sys.argv[3]
	form = sys.argv[4]
	tweet(name,exchange,symbol,form)

