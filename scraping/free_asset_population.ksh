#!/usr/bin/ksh

RUN_DT=$1

if [[ -z $RUN_DT ]]; then
        echo "NO argument! Using today!"
        RUN_DT=`date +%F`
fi


echo $RUN_DT
echo "Scraping Yahoo and Google Data for $RUN_DT"
/home/peter/work/scraping/scrape_free_daily.ksh $RUN_DT

echo "Loading Yahoo and Google Data"
/home/peter/work/scraping/insert_assets_yahoo_bulk.py
/home/peter/work/scraping/insert_assets_google_bulk.py

echo "Archiving"
tar -czf /media/data/investments/data/assets/google/google.nasdaq.$RUN_DT.gz /media/data/investments/data/assets/google/nasdaq/*
tar -czf /media/data/investments/data/assets/yahoo/yahoo.nasdaq.$RUN_DT.gz /media/data/investments/data/assets/yahoo/nasdaq/*

tar -czf /media/data/investments/data/assets/google/google.nyse.$RUN_DT.gz /media/data/investments/data/assets/google/nyse/*
tar -czf /media/data/investments/data/assets/yahoo/yahoo.nyse.$RUN_DT.gz /media/data/investments/data/assets/yahoo/nyse/*

tar -czf /media/data/investments/data/assets/google/google.amex.$RUN_DT.gz /media/data/investments/data/assets/google/amex/*
tar -czf /media/data/investments/data/assets/yahoo/yahoo.amex.$RUN_DT.gz /media/data/investments/data/assets/yahoo/amex/*

echo "Cleaning"
rm /media/data/investments/data/assets/google/nasdaq/*
rm /media/data/investments/data/assets/google/nyse/*
rm /media/data/investments/data/assets/google/amex/*
rm /media/data/investments/data/assets/yahoo/nasdaq/*
rm /media/data/investments/data/assets/yahoo/nyse/*
rm /media/data/investments/data/assets/yahoo/amex/*

echo "Complete"



