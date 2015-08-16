install.packages("reshape", repos='http://cran.us.r-project.org')
install.packages("plyr", repos='http://cran.us.r-project.org')
library(reshape)
library(plyr)

indir = "output"
input_datas = list.files(indir,pattern="*.tsv")
outdir = "output"

for (input_data in input_datas){
    input_file = paste(indir,"/",input_data,sep="")
    output_file = paste(outdir,"/",input_data,sep="")  
    df = read.csv(input_file,sep="\t",row.names=1)  
    # Melt into data frame
    flat = melt(as.matrix(df))
    x = c()
    y = c()
    for (dx in 1:nrow(df)){
      for (dy in 1:ncol(df)){
        x = c(x,dx)
        y = c(y,dy)
      }
    }
    flat$x = x
    flat$y = y
    colnames(flat) = c("probof","given","prob","x","y")
    write.table(flat,file=output_file,sep="\t",row.names=FALSE,col.names=TRUE,quote=FALSE)    
}
