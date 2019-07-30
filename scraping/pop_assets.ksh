

RUN_DT=`date +%F`


fd=`echo $RUN_DT | sed 's/-//g'`
eod_user=`cat ../config.json  | grep eod_user | cut -d":" -f2 | sed 's/"//g' | sed 's/,//g'`
eod_passwd=`cat ../config.json  | grep eod_passwd | cut -d":" -f2 | sed 's/"//g' | sed 's/,//g'`


echo "Running for $RUN_DT"

echo "Scraping"
wget -r -w 2 --random-wait --level 1 --directory-prefix=/media/data/investments/data/assets/landed_data --user=${eod_user} --password=${eod_passwd} ftp://ftp.eoddata.com/
mv /media/data/investments/data/assets/landed_data/ftp.eoddata.com/* /media/data/investments/data/assets/landed_data

wget -r -w 2 --random-wait --level 1 --directory-prefix=/media/data/investments/data/assets/landed_data/Splits --user=${eod_user} --password=${eod_passwd} ftp://ftp.eoddata.com/Splits/
mv /media/data/investments/data/assets/landed_data/Splits/ftp.eoddata.com/Splits/* /media/data/investments/data/assets/landed_data/Splits

wget -r -w 2 --random-wait --level 1 --directory-prefix=/media/data/investments/data/assets/landed_data/Names --user=${eod_user} --password=${eod_passwd} ftp://ftp.eoddata.com/Names/
mv /media/data/investments/data/assets/landed_data/Names/ftp.eoddata.com/Names/* /media/data/investments/data/assets/landed_data/Names

wget -r -w 2 --random-wait --level 1 --directory-prefix=/media/data/investments/data/assets/landed_data/Fundamentals --user=${eod_user} --password=${eod_passwd} ftp://ftp.eoddata.com/Fundamentals/
mv /media/data/investments/data/assets/landed_data/Fundamentals/ftp.eoddata.com/Fundamentals/* /media/data/investments/data/assets/landed_data/Fundamentals

wget -r -w 2 --random-wait --level 1 --directory-prefix=/media/data/investments/data/assets/landed_data/Technical --user=${eod_user} --password=${eod_passwd} ftp://ftp.eoddata.com/Technical/
mv /media/data/investments/data/assets/landed_data/Technical/ftp.eoddata.com/Technical/* /media/data/investments/data/assets/landed_data/Technical

echo "Scrape complete"

echo "Commence Archiving"
tar -czf /media/data/investments/data/assets/compressed_scrape/ohlc_$RUN_DT.gz /media/data/investments/data/assets/landed_data/*.txt
tar -czf /media/data/investments/data/assets/compressed_scrape/splits_$RUN_DT.gz /media/data/investments/data/assets/landed_data/Splits/* 
tar -czf /media/data/investments/data/assets/compressed_scrape/fundamentals_$RUN_DT.gz /media/data/investments/data/assets/landed_data/Fundamentals/* 
tar -czf /media/data/investments/data/assets/compressed_scrape/Names_$RUN_DT.gz /media/data/investments/data/assets/landed_data/Names/* 
tar -czf /media/data/investments/data/assets/compressed_scrape/technicals_$RUN_DT.gz /media/data/investments/data/assets/landed_data/Technical/* 


echo "Moving assets to staging"
cp /media/data/investments/data/assets/landed_data/NASDAQ* /media/data/investments/data/assets/nasdaq
cp /media/data/investments/data/assets/landed_data/AMEX* /media/data/investments/data/assets/amex
cp /media/data/investments/data/assets/landed_data/NYSE* /media/data/investments/data/assets/nyse
cp /media/data/investments/data/assets/landed_data/Names/* /media/data/investments/data/assets/names


for exchange in NYSE NASDAQ AMEX; do cp /media/data/investments/data/assets/landed_data/names/${exchange}.txt /media/data/investments/data/assets/list; done




echo "Inserting data"
/home/peter/work/scraping/insert_assets_eod_bulk.py


echo "Checking for poor data"
/home/peter/work/scraping/daily_asset_scrub.py $RUN_DT

echo "Updating asset_value"
db_user=`cat ../config.json  | grep db_user | cut -d":" -f2 | sed 's/"//g' | sed 's/,//g'`
db_passwd=`cat ../config.json  | grep db_passwd | cut -d":" -f2 | sed 's/"//g' | sed 's/,//g'`
mysql -u $db_user -p${db_passwd}  scrape < /media/data/investments/data/scrub/asset_value_scrub_[1-9]*.sql

echo "Cleaning scrub statements"
mv /media/data/investments/data/scrub/asset_value_scrub_[1-9]*.sql /media/data/investments/data/scrub/loaded


echo "Cleaning staging directories"
/home/peter/work/scraping/clean_assets.ksh

#This reads in the tar file
/home/peter/work/scraping/load_symbols.py $RUN_DT

rm -r /media/data/investments/data/assets/landed_data/*
