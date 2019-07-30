
#!/bin/bash
# From http://calliopesounds.blogspot.com/2011/12/i-have-to-say-again-i-find-gnuplots.html

function show_usage {
 echo \
  usage: $(basename $0) \
  [-x label] \
  [-y label] \
  [-t title] \
  [-s width:height] \
  [-f time-format-strftime] \
  timeseries-input ...
}

function swap {
 echo $2 $1
}

function parse_size {
 W=$(expr $1 : "\\([0-9]*\\):[0-9]*")
 H=$(expr $1 : "[0-9]*:\\([0-9]*\\)")
 echo "$W $H"
}

TIMEFMT="%Y-%m-%dT%H:%M:%S"
XLABEL="Time"
YLABEL="Units"
TITLE="Timeseries"
SIZE=$(swap $(stty size))

while getopts "x:y:t:f:s:h" opt
do
 case $opt in
  x) XLABEL=$OPTARG ;;
  y) YLABEL=$OPTARG ;;
  t) TITLE=$OPTARG ;;
  f) TIMEFMT=$OPTARG ;;
  s) SIZE=$(parse_size $OPTARG) ;;
  h) show_usage ; exit 0 ;;
  *) show_usage ; exit 1 ;;
 esac
done
shift $(expr $OPTIND - 1)

for INPUT in $*
do
 if [ "$INPUT" = "-" ]
 then
  INPUT=$(mktemp /tmp/timeplot.XXXXXXXXXX)
  cat > $INPUT
 fi

 gnuplot <<EOH
  set terminal dumb $SIZE
  set autoscale
  set xdata time
  set timefmt "$TIMEFMT"
  set xlabel "$XLABEL"
  set ylabel "$YLABEL"
  set title "$TITLE"
  plot "$INPUT" using 1:2 with lines
EOH
done

# END

