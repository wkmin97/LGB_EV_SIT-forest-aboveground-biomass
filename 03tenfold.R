library(foreign)
library(stringr)
tenfold_result_11model <- function(ev_nmb,drop_data){
  train_name <- paste0('./train_data_11model_drop',drop_data,'.csv')
  test_name <- paste0('./test_data_11model_drop',drop_data,'.csv')
  train_data<- read.csv(train_name,header = T)
  test_data<- read.csv(test_name,header = T)
  rmse <- function(x,y){
    sqrt(mean((x-y)^2))
  }
  
  result<- data.frame(model=character(),
                      train.rmse=numeric(),
                      train.r=numeric(),
                      test.rmse=numeric(),
                      test.r=numeric())
  
  for(i in 4:length(colnames(train_data))){
    train.r <- cor(train_data[,3],train_data[,i])
    test.r <- cor(test_data[,3],test_data[,i])
    train.rmse <- rmse(train_data[,3],train_data[,i])
    test.rmse <- rmse(test_data[,3],test_data[,i])
    model.name <- str_sub(colnames(train_data)[i],start=11L)
    result[nrow(result)+1,] <- c(model.name,train.rmse,train.r,test.rmse,test.r)
  }
  fname <- paste0('./',ev_nmb,'ev_test_data_11model_result_drop',drop_data,'.csv')
  write.csv(result,file=fname,row.names = F)
}
for (i in 0:3){
  tenfold_result_11model(2,i)
}