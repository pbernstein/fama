RUN_DT='2013-11-01'


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

