
date=$1
next_date=$2

for i in $(find /media/data/investments/data/edgar/forms/rss/loaded/ -maxdepth 1 -type f -newermt $date ! -newermt $next_date) ; do 
		echo "looking for form for $i"
		grep "10-Q" $i >/dev/null
		result=$?
		if [[ $result == 0 ]]
			then
				form="10-Q"
			else
				form="10-K"
		fi
	echo "loading file:"
	echo $i
	echo "As $form for $date"
	/home/peter/work/edgar/reload.py $i $date $form

		
	done
