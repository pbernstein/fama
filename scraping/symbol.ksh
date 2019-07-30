#!/usr/bin/ksh

# Return the exchange and symbol of a Company
# Use me with Care!!!  Do not call me a bunch without waiting, that would be rude

i=$1
STRING=`echo "$i google finance" | sed -e 's/ /%2B/' `;
result=`wget -qO- --user-agent Mozilla "https://www.google.com/search?q=$STRING" | tr " "  "\n" | grep -e NASDAQ -e  NYSE -e AMEX  -e PINK -e OTC | head -1`;
EXCHANGE=`echo $result | cut -d":" -f1`;
SYMBOL=`echo $result | cut -d":" -f2`;
echo $i	
echo $SYMBOL
echo $EXCHANGE



