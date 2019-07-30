

DATE=$1
#FILE=portfolio_value_2012-04-12.log
FILE=/home/ubuntu/work/trade_log/portfolio_value_${DATE}.log
echo "Graphing: $FILE"

if [[ -e $FILE ]]; then
echo "set xdata time ;  set timefmt \"%H:%M:%S.%N\" ; set terminal dumb 60 30 ; plot \"-\" using 1:2 index 0 title \"Balance\" with lines" > /tmp/plot_buffer; cat $FILE | sed -e 's/|/ /g' |  cut -d" " -f2,3 | sed -e 's/\..* / /g' >> /tmp/plot_buffer; gnuplot < /tmp/plot_buffer
fi
