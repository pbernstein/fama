#!/usr/bin/ksh

/home/peter/work/edgar/online_parse.py

RET=$?
if [ $RET != 0 ]; then rm /tmp/online_run; else echo "success"; fi  


