#!/usr/bin/ksh

#curl -s $1 | head -10 > $2
curl -s $1 | head -20 | grep "CONFORMED PERIOD OF REPORT" | cut -d":" -f2   | sed -e 's/\t//g' > $2


