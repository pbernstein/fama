fn=$1
symbol=`cat $fn  | grep "Symbol," | cut -d "," -f2`
form=`cat $fn  | grep "Form," | cut -d "," -f2`
date=`head -2  $fn  | tail -1 |   cut -d "," -f3`
period=`mysql -u root -pstub scrape -e "select eh.period from extract_history eh , dates d where cik  = 866729 and d.date_id = eh.date_id and d.date = \"$date\"" -B | tail -1`
mkdir -p /master/parsed/${date}
cp $fn /master/parsed/${date}/${symbol}_${form}_${period}.csv


