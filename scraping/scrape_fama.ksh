# The month is zero based 

### Backups handled by asset scrape

fama_dir=/media/data/investments/data/fama/
bkp_fama_dir=/media/data/investments/data/fama_bkp/fama_`date +%Y%m%d`

mkdir -p $fama_dir
mkdir -p $bkp_fama_dir

mv ${fama_dir}/* ${bkp_fama_dir}
wget -O ${fama_dir}/F-F_Research_Data_Factors_daily_TXT.zip "http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_TXT.zip"

cd ${fama_dir}
unzip -u F-F_Research_Data_Factors_daily_TXT.zip

line_count=`wc -l F-F_Research_Data_Factors_daily.txt | cut -d" " -f1`
start=`echo "$line_count - 2" | bc -l`
end=`echo "$start - 5" | bc -l`
head -$start F-F_Research_Data_Factors_daily.txt  | tail -$end | awk '{print $1,",",$2,",",$3,",",$4,",",$5}' | sed 's/ //g' > F-F_Research_Data_Factors_daily.load
dos2unix F-F_Research_Data_Factors_daily.load




