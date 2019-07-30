#!/usr/bin/ksh




#tfile = tarfile.open("/media/data/investments/data/edgar/forms/eod/forms/eod_20130401.tar.gz")
#tfile = tarfile.open("/media/data/investments/data/edgar/forms/eod/form_bkp/eod_20130401.tar.gz")
#tfile.extractall()  

def extract(file):
	tfile = tarfile.open(file)
	print tfile.extractall()  
	tfile.close()



if __name__ == '__main__':
	#file = sys.argv[1]
	#file = "/media/data/investments/data/edgar/forms/eod/forms/eod_20130401.tar.gz"
	file = "/media/data/investments/data/edgar/forms/eod/form_bkp/eod_20130401.tar.gz"
	print file
        extract(file)
	



