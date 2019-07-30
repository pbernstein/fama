#!/usr/bin/python


import tarfile
#from subprocess import call


#tfile = tarfile.open("/media/data/investments/data/edgar/forms/eod/forms/eod_20130401.tar.gz")
#tfile.extractall(path="/")  
#call(["tar","-xzf","/media/data/investments/data/edgar/forms/eod/forms/eod_20130401.tar.gz",)
tfile = tarfile.open("/media/data/investments/data/edgar/forms/eod/forms/eod_20130401.tar.gz")   
tfile.extractall(path="/")         



