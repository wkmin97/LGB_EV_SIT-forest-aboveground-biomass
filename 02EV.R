library(fields)
library(vegan)
library(MASS)
library(spdep)
library(sp)
extract_meigen <- function(coords, model, threshold = 0.25, k=NULL){
  D <- rdist(coords)
  h <- max(spantree(D)$dist)
  
  if(model == "exp"){
    C <- ifelse( D < h, exp( -D / h ), 0)
  }
  else if(model == "gau"){
    C <- ifelse( D < h, exp( -(D / h) ^ 2 ), 0)
  }
  else if(model == "sph"){
    C	<- ifelse( D < h , 1 - 1.5 * (D / h ) + 0.5 * ( D / h ) ^ 3, 0 )
  }
  else if(model == "gau2"){
    C <- exp( -(D / h) ^ 2 )
  }
  else if(model == "gau3"){
    C <- exp( -0.5 * (D / h) ^ 2 )
  }
  else if(model == 'k' && !is.null(k)){
    knearest <- knearneigh(coordinates(coords), k = k)
    C <-  nb2mat(knn2nb(knearest), style = "B")
    if(isSymmetric(C)==FALSE){
      C <- 0.5*(C+t(C))
    }
  }
  else{
    stop("弟弟，你玩我吧，没有这个模型呀！")
  }
  
  diag(C) <- 0
  n <- dim(C)[1]
  #中心化centering
  MCM <- (diag(n) - c(rep(1,n)) %*% t(c(rep(1,n)))/n) %*% C %*% (diag(n) - c(rep(1,n)) %*% t(c(rep(1,n)))/n)
  eigenC <- eigen( MCM )
  eigenC$values <- Re( eigenC$values )
  eigenC$vectors <- Re( eigenC$vectors )
  ev <- eigenC$vectors[, eigenC$values/max(eigenC$values) >= threshold]
  ev_v <- eigenC$values[ eigenC$values/max(eigenC$values) >= threshold]
  return( list(ev=ev, ev_v=ev_v) )
}

data <- read.csv('./biomass_metrics_19.csv',header = T)
meig <- extract_meigen(coords=data[,c('POINT_X','POINT_Y')], model='gau', threshold = 0.25)
EV <- data.frame(meig$ev)
colnames(EV)<-paste("EV",1:NCOL(EV),sep="")
data_ev <- cbind(data,EV)
ev2_data <- data.frame(data[,2])
for (i in 5:length(colnames(data))){
  for(j in 1:length(colnames(EV))){
    SVC<-data[,i]*EV[,j]
    ev2_data <- data.frame(ev2_data,SVC)
  }
}
colnames(ev2_data)[2:2406]<-paste("SVC",1:NCOL(EV),sep="")
data_2ev <- cbind(data_ev,ev2_data[2:2406])
write.csv(data_2ev,file='biomass_metrics_allev_svc_19.csv',row.names = F)

library(MASS)
library(stringr)
y <- data[['b1_agbd_19']]
xs  <- cbind(y,EV)
model.lm.ev<-lm(y~.,data = xs)
ev <- predict(model.lm.ev,xs)
xs  <- cbind(y,ev2_data[2:2406])
model.lm.svc<-lm(y~.,data = xs)
svc <- predict(model.lm.svc,xs)
data_metrics <- cbind(data,ev,svc)
write.csv(data_metrics,file='biomass_metrics_all_19.csv',row.names = F)

data <- read.csv('./biomass_metrics_all_19.csv',header = T)
tenfold_data_pred <- function(){
  id <- rownames(data)
  data <- cbind(id,data)
  ind <- sample(10, nrow(data), replace=T)
  for (i in 1:10){
    data.train <- data[ind!=i,]
    train.data.name <- paste('train_data_',i,'.csv',sep='')
    write.csv(data.train,file=paste0('tenfold_data/',train.data.name),row.names = F)
    data.test <- data[ind==i,]
    test.data.name <- paste('test_data_',i,'.csv',sep='')
    write.csv(data.test,file=paste0('tenfold_data/',test.data.name),row.names = F)
  }
}
tenfold_data_pred()
