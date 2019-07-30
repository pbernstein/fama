#!/usr/bin/python

import os
import sys
import twitter


#def tweet(name, exchange, symbol, form):
#	my_auth = twitter.OAuth('1059455906-G3z4sa3DGprHTvVxzOXWXMDEKOUXrr1ZbMOeKJa','6uV2rEllYtaddrY5ezca3kGesL6WUSf6Rbk7zHPFWk','XOzC2Nk6kQClQycgQ6J1LQ','404BT9oqUumtVw0OfrThVWdzo61RV5XRIvuud8hhDA8')
#	twit = twitter.Twitter(auth=my_auth)
#	twit.statuses.update(status=name.replace("_"," ")+" "+exchange+":"+symbol+" "+form+" available for download")
#
#
#if __name__ == '__main__':
#	name = sys.argv[1]
#	exchange = sys.argv[2]
#	symbol = sys.argv[3]
#	form = sys.argv[4]
#	tweet(name,exchange,symbol,form)

api = twitter.Twitter.Api()
statuses = api.GetPublicTimeline()
print [s.user.name for s in statuses] [u'Instrumental Data']

