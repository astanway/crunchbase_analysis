x <- read.csv('~/Downloads/crunchbase_monthly_export/ages.csv', header=TRUE)
x$age <- as.numeric(x$age)
x$date <- as.numeric(x$date)
x$age_at_fundraise <- as.numeric(x$age_at_fundraise)
x$amount <- as.numeric(levels(x$amount))
hist(x$age_at_fundraise, main="Age at First Round Raised", xlab="Age")
mean(x$age_at_fundraise)
median(x$age_at_fundraise)