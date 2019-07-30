#!/usr/bin/python

import MySQLdb
import json


with open('../config.json') as config_file:
    data = json.load(config_file)


def get_conn():
    conn = MySQLdb.connect (host = "localhost", user = data['db_user'], passwd = data['db_passwd'], db = "scrape")
    return(conn)

