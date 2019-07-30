#!/usr/bin/ksh

AMOUNT=$1
TRADE_DATE=$2

db_user=`cat ../config.json  | grep db_user | cut -d":" -f2 | sed 's/"//g' | sed 's/,//g'`
db_passwd=`cat ../config.json  | grep db_passwd | cut -d":" -f2 | sed 's/"//g' | sed 's/,//g'`


TRADE_DATE_ID=`mysql -u ${db_user} -p${db_passwd} scrape -e "select date_id from dates where date = '$TRADE_DATE'" | tail -1`

RESULT=`./run_all.py $AMOUNT $TRADE_DATE 1800 30 0.000 2 1 20 "Y"`
PREAMBLE="mysql -u ${db_user} -p${db_passwd} scrape -e"

BUY=`echo $RESULT | cut -d\| -f2`
SELL=`echo $RESULT | cut -d\| -f4`

#echo $BUY
#echo $SELL

for i in $BUY;do
	ASSET_NAME=`echo $i | cut -d, -f1 | sed -e 's/-/ PR/'`
	SHARES=`echo $i | cut -d, -f2`
	EXCHANGE=`echo $i | cut -d, -f3`
	#echo "an = $asset_name"
	#echo "shares = $shares"
  	INSERT=`echo "$PREAMBLE \"insert into trade (trade_date_id, asset, exchange,  action, shares, status, type) values ($TRADE_DATE_ID, \\\\\"""$ASSET_NAME\\\\\""", \\\\\"""$EXCHANGE\\\\\""", \\\\\"""BUY\\\\\""", $SHARES, 0, \\\\\"""ENTER\\\\\""")\""`
	ssh < MY AWS MACHINE > $INSERT
	if [ $? != 0 ];then
		echo "Something went wrong"
	fi;

  	INSERT=`echo "$PREAMBLE \"insert into trade (trade_date_id, asset, action, shares, status, type) values ($TRADE_DATE_ID, \\\\\"""$ASSET_NAME\\\\\""", \\\\\"""SELL\\\\\""", $SHARES, 0, \\\\\"""EXIT\\\\\""")\""`
	ssh < MY AWS MACHINE > $INSERT
	if [ $? != 0 ];then
		echo "Something went wrong"
	fi;
  	


done

for i in $SELL;do
        ASSET_NAME=`echo $i | cut -d, -f1 | sed -e 's/-/ PR/'`
        SHARES=`echo $i | cut -d, -f2`
        #echo "an = $asset_name"
        #echo "shares = $shares"
  	INSERT=`echo "$PREAMBLE \"insert into trade (trade_date_id, asset, exchange,  action, shares, status, type) values ($TRADE_DATE_ID, \\\\\"""$ASSET_NAME\\\\\""", \\\\\"""$EXCHANGE\\\\\""", \\\\\"""SELL\\\\\""", $SHARES, 0, \\\\\"""ENTER\\\\\""")\""`
	ssh < MY AWS MACHINE > $INSERT
	if [ $? != 0 ];then
		echo "Something went wrong"
	fi;

  	INSERT=`echo "$PREAMBLE \"insert into trade (trade_date_id, asset, action, shares, status,type) values ($TRADE_DATE_ID, \\\\\"""$ASSET_NAME\\\\\""", \\\\\"""BUY\\\\\""", $SHARES, 0, \\\\\"""EXIT\\\\\""")\""`
	ssh < MY AWS MACHINE > $INSERT
	if [ $? != 0 ];then
		echo "Something went wrong"
	fi;
done
	

