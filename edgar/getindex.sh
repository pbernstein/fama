#!/bin/sh

# Downloads an index file from the SEC FTP server.
# Usage: sh getindex.sh YEAR QUARTER
# where YEAR is 2005, 2006, etc...
# and QUARTER is 1, 2, 3, or 4

YEAR=$1
QTR=$2

#wget -O data/indexes/$YEAR.$QTR ftp://ftp.sec.gov/edgar/full-index/$YEAR/QTR$QTR/master.idx
wget -O /media/data/investments/data/edgar/indexes/$YEAR.$QTR ftp://ftp.sec.gov/edgar/full-index/$YEAR/QTR$QTR/master.idx
