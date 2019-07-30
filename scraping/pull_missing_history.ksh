RUN_DT='2013-11-01'


fd=`echo $RUN_DT | sed 's/-//g'`
echo "Running for $RUN_DT"

echo "Scraping"
wget -r -w 2 --random-wait --level 1 --directory-prefix=/media/data/investments/data/assets/landed_data/History --user=eod_user --password=eod_pass ftp://ftp.eoddata.com/History/AMEX*
wget -r -w 2 --random-wait --level 1 --directory-prefix=/media/data/investments/data/assets/landed_data/History --user=eod_user --password=eod_pass ftp://ftp.eoddata.com/History/NYSE*
wget -r -w 2 --random-wait --level 1 --directory-prefix=/media/data/investments/data/assets/landed_data/History --user=eod_user --password=eod_pass ftp://ftp.eoddata.com/History/NASDAQ*
mv /media/data/investments/data/assets/landed_data/Technical/ftp.eoddata.com/History/* /media/data/investments/data/assets/landed_data/History


