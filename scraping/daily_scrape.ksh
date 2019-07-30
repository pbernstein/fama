RUN_DT=`date +%F`

echo "Paid scrape"
/home/peter/work/scraping/pop_assets.ksh  # WILL ONLY RUN ON RUN_DT

echo "Free scrape"
/home/peter/work/scraping/free_asset_population.ksh  #DEFAULTS TO RUN_DT
echo "Scrubbing Assets"
/home/peter/work/scraping/daily_asset_scrub.py $RUN_DT

echo "Updating asset_value"
db_user=`cat ../config.json  | grep db_user | cut -d":" -f2 | sed 's/"//g' | sed 's/,//g'`
db_passwd=`cat ../config.json  | grep db_passwd | cut -d":" -f2 | sed 's/"//g' | sed 's/,//g'`


mysql -u $db_user -p${db_passwd} scrape < /media/data/investments/data/scrub/asset_value_scrub_[1-9]*.sql

echo "Cleaning scrub statements"
mv /media/data/investments/data/scrub/asset_value_scrub_[1-9]*.sql /media/data/investments/data/scrub/loaded

