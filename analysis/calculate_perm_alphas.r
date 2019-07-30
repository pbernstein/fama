

args <- commandArgs(TRUE)
data_file = args[1]
reg_file = args[2]

x_all=read.csv(file=data_file,head=TRUE,sep=',')
x_data=x_all[,-1] # remove the date row

print(x_data) 


for (i in 1:length(x_data)) {
 r<- coef(summary(lm(x_data[,names(x_data)[i]]~x_data[,"mkt.rf"]+x_data[,"smb"]+x_data[,"hml"])))
 if (i == 1)
 final = c(names(x_data)[i], r["(Intercept)","Estimate"], abs(r["(Intercept)","t value"]))
 else
 final = rbind(final,c(names(x_data)[i], r["(Intercept)","Estimate"], abs(r["(Intercept)","t value"])))
}


names(final)[1] = "Asset"
names(final)[2] = "Alpha"
names(final)[3] = "T"


assets = c()
for (i in 1:(length(final)/3)) {
	assets = c(assets,final[i,]) 
}



assets
write(assets,ncolumns=3,reg_file)
