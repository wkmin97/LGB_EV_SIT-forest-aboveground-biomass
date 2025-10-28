rm(list=ls()); gc();
library(foreign)
library(stringr)
library(base)

rename_dbf_mean_9 <-function(dfname,dname){
  d <- read.dbf(dfname)
  names(d)[9] <- dname
  return(d)
}

rename_dbf_mean_11 <-function(dfname,dname){
  d <- read.dbf(dfname)
  names(d)[11] <- dname
  return(d)
}
###
path_dbf="G:/project/USA_west/metrics/2019"
list_dbf=c(dir(path_dbf,pattern = ".dbf"))
list_dbf_9 = c(list_dbf[1:11],list_dbf[13:14],list_dbf[16:18],list_dbf[20:28],list_dbf[32],list_dbf[34:36])
list_dbf_11 = c(list_dbf[12],list_dbf[15],list_dbf[19],list_dbf[29:31],list_dbf[33])
ip_name <- str_sub(list_dbf_11[1],start=1L,end=-5L)
indbf <- rename_dbf_mean_11(list_dbf_11[1],ip_name)
mergedata <- data.frame(indbf[1],indbf[3],indbf[9:10],indbf[2],indbf[11])

  for (j in 2:length(list_dbf_11)){
    ip_name <- str_sub(list_dbf_11[j],start=1L,end=-5L)
    indbf <- rename_dbf_mean_11(list_dbf_11[j],ip_name)
    mergedata <- data.frame(mergedata,indbf[11])
    print(paste0(' done:  #', j,': dbf ',ip_name))
  }
for (i in 1:length(list_dbf_9)){
  ip_name <- str_sub(list_dbf_9[i],start=1L,end=-5L)
  indbf <- rename_dbf_mean_9(list_dbf_9[i],ip_name)
  mergedata <- data.frame(mergedata,indbf[9])
  print(paste0(' done:  #', i,': dbf ',ip_name))
}
colnames(mergedata)
setwd('E:/program/biomass_2024/biomass19')
write.csv(mergedata,file='biomass_metrics_19.csv',row.names = F)
write.table(mergedata,file='biomass_metrics_19.txt',row.names = F)




path_csv <- 'G:/NEON/metrics_csv'
setwd(path_csv)
list_csv <- paste0(list_tiles,'.txt')
merge_csv <- data.frame()


###test one
csv_data <- read.table(list_csv[1],head=T)
merge_csv <- rbind(merge_csv,csv_data)

csvname <- paste(list_tiles[i],".csv",sep='')
txtname <- paste(list_tiles[i],".txt",sep='')
write.csv(csv_data,file=csvname,row.names = F)
write.table(csv_data,file=txtname,row.names = F)

