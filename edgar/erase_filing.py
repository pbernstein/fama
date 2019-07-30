#!/usr/bin/python

#
# Usage:


import sys
import MySQLdb






def erase(eh_sk):

	if eh_sk == "":
		sys.exit(1)

	conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "stub", db = "scrape")
	cursor = conn.cursor ()
	cursor.execute(" delete from extract_history where eh_sk = "+str(eh_sk))
	cursor.execute(" delete from gaap_value where eh_sk = "+str(eh_sk))
	cursor.execute(" delete from ins_value where eh_sk = "+str(eh_sk))

	cursor.close()
	conn.commit()
	conn.close()


if __name__ == '__main__':
        eh_sk = sys.argv[1]
	erase(eh_sk)

