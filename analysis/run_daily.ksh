#!/usr/bin/ksh

amount=$1
date=$2

echo "Predicting with $amount for $date"

/home/peter/work/analysis/run_all.py $amount $date 4 30 .0025 2 1 20 | grep manual > /tmp/predict_$date.ksh

echo "./open_orders.py " >> /tmp/predict_$date.ksh


