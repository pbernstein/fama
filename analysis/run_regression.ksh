#R CMD BATCH --args arg1=abc calculate_alphas.r
#R CMD BATCH --vanilla --args stuff calculate_alphas.r
#cat calculate_alphas.r | R --vanilla --args stuff 
 

R --vanilla --args $1 $2 < /home/peter/work/analysis/calculate_alphas.r > /home/peter/work/analysis/calculate_alphas.r.Rout

