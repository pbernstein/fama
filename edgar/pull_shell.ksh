#!/usr/bin/ksh

/home/peter/work/edgar/pull_daily_xbrl.py

RET=$?
if [ $RET != 0 ]; then rm /tmp/pull_run; else echo "success"; fi  


