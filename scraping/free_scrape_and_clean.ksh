RUN_DT=`date +%F`

echo "Free scrape"
/home/peter/work/scraping/free_asset_population.ksh  #DEFAULTS TO RUN_DT
echo "Scrubbing Assets"
/home/peter/work/scraping/daily_asset_scrub.py $RUN_DT

echo "Updating asset_value"
mysql -u update_user -pupdate_pw scrape < /media/data/investments/data/scrub/asset_value_scrub_[1-9]*.sql

echo "Cleaning scrub statements"
mv /media/data/investments/data/scrub/asset_value_scrub_[1-9]*.sql /media/data/investments/data/scrub/loaded

