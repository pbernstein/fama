
if [[ $1 -eq "" ]];then 
	RUN_DT=`date +%F`
else
	RUN_DT=$1
fi


echo "Running for " $RUN_DT
fd=`echo $RUN_DT | sed 's/-//g'`

echo "Checking for poor data"
/home/peter/work/scraping/daily_asset_scrub.py $RUN_DT

echo "Update stats:"
ls -l /media/data/investments/data/scrub/asset_value_scrub_$RUN_DT.sql


echo "Updating asset_value"
db_user=`cat ../config.json  | grep db_user | cut -d":" -f2 | sed 's/"//g' | sed 's/,//g'`
db_passwd=`cat ../config.json  | grep db_passwd | cut -d":" -f2 | sed 's/"//g' | sed 's/,//g'`
mysql -u $db_user -p${db_passwd} scrape < /media/data/investments/data/scrub/asset_value_scrub_$RUN_DT.sql

echo "Cleaning scrub statements"
mv /media/data/investments/data/scrub/asset_value_scrub_[1-9]*.sql /media/data/investments/data/scrub/loaded


