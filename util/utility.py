
def clean_name(name):
	tmp = name.replace(" ","_").replace("/","-").replace(".","").replace("&","AND").replace(",","").replace("(","").replace(")","").replace('"','').replace("'","").upper()
	if tmp[-1] == "-":
		tmp = tmp[:-1]
	return tmp


	

def get_date_id(cursor,date):
	cursor.execute(" select date_id from dates where date = \""+str(date)+"\"")
        row = cursor.fetchone()
        date_id = row[0]
	return date_id

def get_symbol(cursor,date_id, cik):
	print "select exchange, symbol from symbol where "+str(date_id)+" > start_date_id and "+str(date_id)+" < end_date_id and cik = \""+str(cik)+"\" order by exchange desc, length(symbol)  limit 1"
	cursor.execute("select exchange, symbol from symbol where "+str(date_id)+" > start_date_id and "+str(date_id)+" < end_date_id and cik = \""+str(cik)+"\" order by exchange desc, length(symbol)  limit 1")
        result = cursor.fetchone()
	try:
		print "here"
		exchange = result[0]
		symbol = result[1]
	except:
		try:
			cursor.execute("select exchange, symbol from csi_symbols where "+str(date_id)+" = date_id and cik = \""+str(cik)+"\" limit 1")
			print "select exchange, symbol from csi_symbols where "+str(date_id)+" = date_id and cik = \""+str(cik)+"\" limit 1"
			result = cursor.fetchone()
			exchange = result[0]
			symbol = result[1]

		except:
			exchange = "NA"
			symbol = "NA"

	return symbol, exchange



