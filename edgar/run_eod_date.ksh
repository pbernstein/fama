


run_dt=$1

for i in $run_dt; do /home/peter/work/edgar/pull_eod_xbrl.py  ${i} > /home/peter/logging/eod_${i}.log; done 

tar -czf /media/data/master/parsed/${run_dt}.tar.gz  /media/data/master/parsed/${run_dt}/*
rm -r  /media/data/master/parsed/${run_dt}
scp -i ~/bin/testserver.pem /media/data/master/parsed/${run_dt}.tar.gz   ubuntu@50.19.103.62:/master/parsed
ssh -i ~/bin/testserver.pem ubuntu@50.19.103.62 "tar -xzmf /master/parsed/${run_dt}.tar.gz -C /master/parsed/${run_dt} --strip-components 5"
ssh -i ~/bin/testserver.pem ubuntu@50.19.103.62 "rm -r /master/parsed/${run_dt}.tar.gz "



tar -czf /media/data/master/filings/${run_dt}.tar.gz  /media/data/master/filings/${run_dt}/*
rm -r  /media/data/master/filings/${run_dt}
scp -i ~/bin/testserver.pem /media/data/master/filings/${run_dt}.tar.gz   ubuntu@50.19.103.62:/master/filings
ssh -i ~/bin/testserver.pem ubuntu@50.19.103.62 "tar -xzmf /master/filings/${run_dt}.tar.gz -C /master/filings/${run_dt} --strip-components 5"
ssh -i ~/bin/testserver.pem ubuntu@50.19.103.62 "rm -r /master/filings/${run_dt}.tar.gz "




