
eh=$1
sed -e "s/template/$eh/g" template_prices.sql > /tmp/plot_sql
sed -e "s/template/$eh/g" template_filing.sql > /tmp/filing_sql
sed -e "s/template/$eh/g" template_change.sql > /tmp/change_sql

db_user=`cat ../config.json  | grep db_user | cut -d":" -f2 | sed 's/"//g' | sed 's/,//g'`
db_passwd=`cat ../config.json  | grep db_passwd | cut -d":" -f2 | sed 's/"//g' | sed 's/,//g'`

mysql -u $db_user -p${db_passwd} scrape  -N < /tmp/plot_sql  > /tmp/plot_data
mysql -u $db_user -p${db_passwd} scrape  -N < /tmp/filing_sql  > /tmp/filing_data
mysql -u $db_user -p${db_passwd} scrape  -N < /tmp/change_sql  > /tmp/change_data

symbol=`cat /tmp/change_data` 
if [[ symbol -eq "" ]]; then 
symbol=4
#exit 1
fi

echo "symbol = $symbol"




# Use
# select p.value from ins_map p where im.symbol = p.symbol and im.attribute = p.attribute and im.form = p.form and im.date_ d > p.date_id order by date_id desc limit 1  )
# to determine if the previous filing was in the same direction. if it was, then make linetype 3, if not, lintime 4

 gnuplot <<EOH
  set terminal dumb 
  set autoscale
  set xdata time
  set timefmt "%H:%M"
  set xlabel "Time"
  set ylabel "Price"
  set title "Historical Price"
  plot "/tmp/plot_data" using 1:2 with lines, "/tmp/filing_data"  using 1:2 with impulses linetype $symbol
EOH


#2 - #  DOWN
#3 - $  UP
#4 - %   NO PRIOR ATTRIBUTE
#5 - @
#6 - &
#7 - =

