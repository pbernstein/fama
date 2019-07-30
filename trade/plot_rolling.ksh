

DATE=$1

 echo "set xdata time ;  set timefmt \"%Y-%m-%d\" ; set terminal dumb 60 30 ; plot \"-\" using 1:2 index 0 title \"Balance\" with lines" > test; cat rolling_balance.dat_temp | sed -e 's/|/ /g' | sed -e 's/://g' | cut -d" " -f1,3 | sed -e 's/\..* / /g' >> test; gnuplot < test > rolling_${DATE}.dat

cat rolling_${DATE}.dat
