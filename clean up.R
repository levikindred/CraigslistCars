library(class)


carData <- read.csv("C:\\Users\\Levi\\Desktop\\Craigslist\\test case\\minneapoliskeyData.csv", header = FALSE)
carData[] <- lapply(carData, as.character)
colnames(carData) <- c("ID", "City", "model", "make", "year", "price", "miles", "cyl", "title", "trans")


rowsToRemove <- c()
for (i in 1:length(carData$ID)){
  if(carData$model[i] == "None" || carData$year[i] == "None" || carData$price[i] == "None" || carData$miles[i] == "None"){
    rowsToRemove <- c(rowsToRemove, i)
  }
}

carData <- carData[-rowsToRemove, ]

carData <- carData[!duplicated(carData[, 2:10]), ]

carData$miles <- as.numeric(carData$miles)
rowsToRemove <- c()
for (i in 1:length(carData$ID)){
  if(carData$miles[i] < 10000){
    rowsToRemove <- c(rowsToRemove, i)
  while(carData$miles[i] > 1000000)
    carData$miles[i] <- carData$miles[i] / 10
  }
}
carData <- carData[-rowsToRemove, ]

#write.csv(carData, "C:\\Users\\Levi\\Desktop\\Craigslist\\test case\\minneapoliskeyDataCleaned.csv", row.names = F)


models <- unique(carData$model)
modelCounts <- rep(0, length(models))

for (i in 1:length(carData$model)){
  m <- match(carData$model[i], models)
  modelCounts[m] = modelCounts[m] + 1
}

models <- models[order(modelCounts, decreasing = T)]
modelCounts <- sort(modelCounts, decreasing = T)