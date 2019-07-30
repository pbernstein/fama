#!/usr/bin/ksh
date=$1
quarter=$2

for i in $date; do /home/peter/work/edgar/pull_csi_xbrl.py  ${i} ${quarter} > /home/peter/logging/csi_eod_${i}.log; done


