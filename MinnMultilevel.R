library(lme4)

regData <- read.csv("C:\\Users\\Levi\\Desktop\\Craigslist\\minneapolisCombined.csv")

regData$year <- 2017 - regData$year
regData$price <- as.numeric(as.character(regData$price))
regData$makeModel <- paste(as.character(regData$make), as.character(regData$model))
regData$miles <- as.numeric(as.character(regData$miles))
regData$miles[regData$miles < 1000 | regData$miles > 1000000] <- NA
regData$miles <- log(regData$miles)
regData$cyl <- as.numeric(as.character(regData$cyl))

m <- lmer(price ~ year + miles + cyl + title + trans + (1 | makeModel), data = regData)



predData <- regData[complete.cases(regData), ]

predData$predictions <- predict(m)
predData$diff <- predData$price - predData$predictions
