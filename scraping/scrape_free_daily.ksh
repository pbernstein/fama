#!/bin/ksh

DL_DATE=$1

if [[ $DL_DATE = "" ]]; then
	echo "PASS IN A DATE! i.e. $0 2012-03-02"
	exit
fi


YEAR=`echo $DL_DATE | cut -d"-" -f1`
MONTH=`echo $DL_DATE | cut -d"-" -f2`
DAY=`echo $DL_DATE | cut -d"-" -f3`


# FOR YAHOO DATES, THE MONTH is -1, EVERYTHING ELSE IS UNCHANGED
y_year=$YEAR
y_month=`echo "$MONTH - 1" | bc`
y_day=$DAY

y_from_year=$y_year
y_from_month=$y_month
y_from_day=$y_day

y_to_year=$y_year
y_to_month=$y_month
y_to_day=$y_day


# FOR GOOGLE DATES, MONTH IS IN ABBR FORMAT
g_year=$YEAR
MONTHS=(Filler Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec)
g_month=`echo ${MONTHS[${MONTH}]}`
g_day=$DAY

g_from_year=$g_year
g_from_month=$g_month
g_from_day=$g_day

#g_from_year=2012
#g_from_month="Mar"
#g_from_day=21

g_to_year=$g_year
g_to_month=$g_month
g_to_day=$g_day



for exchange in nasdaq nyse amex; do
	for asset in $(cat /media/data/investments/data/assets/list/` echo ${exchange} | tr '[a-z]' '[A-Z]'`.txt | sed -e 's/\t/ /g' | cut -d" " -f1);do
			wget -qO /media/data/investments/data/assets/google/${exchange}/scrape_${asset} "http://www.google.com/finance/historical?q=${asset}&startdate=${g_from_month} ${g_from_day}, ${g_from_year}&enddate=${g_month} ${g_day}, ${g_year}&output=csv"
			wget -qO /media/data/investments/data/assets/yahoo/${exchange}/scrape_${asset} "http://ichart.finance.yahoo.com/table.csv?s=${asset}&a=${y_from_month}&b=${y_from_day}&c=${y_from_year}&d=${y_to_month}&e=${y_to_day}&f=${y_to_year}&g=d&ignore=.csv"

			sleep 1
		done

	# Remove all 0 byte files
	find /media/data/investments/data/assets/google/${exchange} -name "scrape_*"  -type f -size 0 -exec rm {} \;
	find /media/data/investments/data/assets/yahoo/${exchange} -name "scrape_*"  -type f -size 0 -exec rm {} \;

	# Remove all 3 byte files # Known garbage
	find /media/data/investments/data/assets/google/nasdaq -name "scrape_*"  -type f -size 3c -exec rm {} \;
	find /media/data/investments/data/assets/google/nasdaq -name "scrape_*"  -type f -size 35c -exec rm {} \;
done





