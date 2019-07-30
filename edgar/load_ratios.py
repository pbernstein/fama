#!/usr/bin/python

import MySQLdb
import buckets
import types


Dividends = []
for i in """
paymentsofdividendscommonstock
paymentsofdividends
dividends
paymentsofordinarydividends
dividendscash
dividendscommonstockcash
dividendscommonstock
commonstockdividendspersharedeclared
dividendspayablecurrentandnoncurrent
equitymethodinvestmentdividendsordistributions
dividendspayablecurrent
dividendspreferredstockcash
dividendspreferredstock
paymentsofdividendspreferredstockandpreferencestock
sharebasedcompensationarrangementbysharebasedpaymentawardfairvalueassumptionsexpecteddividendrate
""".split("\n"):
        if len(i) > 1:
                Dividends.append(i)


Inventory = []

for i in """
inventorynet
inventoryfinishedgoods
inventorygross
""".split("\n"):
        if len(i) > 1:
                Inventory.append(i)


columns = {}

for i in globals():
        try:
                assert isinstance(globals()[i], types.ListType)
                columns[i] =  globals()[i]
        except:
                pass


conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
cursor = conn.cursor ()


for i in columns:
		count = 1
		#print i#, columns[i]
		for j in columns[i]:
			cursor.execute("insert into imap (`i_attribute`, `filing_attribute`, `source`, `type`, `priority`) values ("+",".join(map(str,["\""+i+"\"", "\""+j+"\"", "\"x\"", "\"u\"", count]))+")")
			count = count + 1
			

conn.commit()
cursor.close()
conn.close()

