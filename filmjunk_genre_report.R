rm(list = ls(all = T))
closeAllConnections()
require(plyr)
require(data.table)
setwd("/Users/Matt/Dropbox/github/scrapes/temp/")

#import ratings
ratings = read.table("/Users/Matt/Dropbox/github/scrapes/temp/filmjunk_ratings.csv", header = T, sep = '\t')

#reshape long to wide
ratings = reshape(ratings, idvar = c("movie", "rater"), direction = "wide", timevar = "key")

#normalize ratings
ratings$rating = ratings$value.rating/ratings$value.system
ratings = ratings[ , -c(3, 4)]

#import film genres
genres = read.table('/Users/Matt/Dropbox/github/scrapes/temp/movie_genres.csv', header = T, sep = '\t')
dt = data.table(genres)
dt[, id := seq_len(.N), by = movie]
genres = as.data.frame(dt)
rm(dt)

genres = reshape(genres, idvar = "movie", direction = "wide", timevar = "id")
genres = rename(genres, c("genre.1" = "genre1", "genre.2" = "genre2", "genre.3" = "genre3"))

#create genre dummies
require(dummies)

#create dummies for first var
dum = as.data.frame(dummy(genres$genre1))
#...second var
dum2 = as.data.frame(dummy(genres$genre2))
#...third var
dum3 = as.data.frame(dummy(genres$genre3))

#remove NA columns
dum2 = dum2[ , -17]
dum3 = dum3[ , -11]

#fill in missing genres
dum$"genre1)Animation" = 0
dum$"genre1)Biography" = 0
dum$"genre1)Short" = 0

dum2$"genre2)Animation" = 0
dum2$"genre2)Music" = 0
dum2$"genre2)Musical" = 0
dum2$"genre2)Short" = 0
dum2$"genre2)Sport" = 0
dum2$"genre2)War" = 0
dum2$"genre2)Western" = 0

dum3$"genre3)Family" = 0
dum3$"genre3)Fantasy" = 0
dum3$"genre3)History" = 0
dum3$"genre3)Music" = 0
dum3$"genre3)Musical" = 0
dum3$"genre3)Romance" = 0
dum3$"genre3)Sci-Fi" = 0
dum3$"genre3)Short" = 0
dum3$"genre3)Sport" = 0
dum3$"genre3)Thriller" = 0
dum3$"genre3)War" = 0
dum3$"genre3)Western" = 0

genres = cbind(genres, dum, dum2, dum3)
rm(dum, dum2, dum3)

#create final dummies
for (g in levels(genres$genre1)) {
  s = paste0('genre1)', g)
  s2 = paste0('genre2)', g)
  s3 = paste0('genre3)', g)
  genres[[g]] = genres[[s]] + genres[[s2]] + genres[[s3]] 
}

genres = genres[ , -(5:70)]

#merge ratings and genres
master = merge(ratings, genres, by = "movie")

common = ddply(master, .(movie), nrow)
common = as.data.frame(common[ which(common$V1 == 3), 1])
common = rename(common, c("common[which(common$V1 == 3), 1]" = "movie"))

master = merge(master, common, by = "movie")

# #weight genre dummies
# master$gSum = apply(X = master[, 7:28], MARGIN = 1, FUN = sum)
# for (g in levels(genres$genre1)) {
#   master[[g]] = master[[g]]/master[, 29] 
# }

master = master[, -c(1, 4:6, 29)]



#correlation matrix
cor(master[, 3:24])

  
  

#Frank model##############################################################
f_d = master[ which(master$rater == 'Frank'), ]
f_d = f_d[ , -1]

#average rating
mean(f_d$rating)
sd(f_d$rating)

ols = lm(rating ~ ., data = f_d)
sink(file = 'results_output.txt')
summary(ols)
closeAllConnections()

  
  
#sean model##############################################################
s_d = master[ which(master$rater == 'Sean'), ]
s_d = s_d[ , -1]

#average rating
mean(s_d$rating)
sd(s_d$rating)

ols = lm(rating ~ ., data = s_d)
sink(file = 'results_output.txt', append = T)
summary(ols)
closeAllConnections()

  

#jay model##############################################################
j_d = master[ which(master$rater == 'Jay'), ]
j_d = j_d[ , -1]

#average rating
mean(j_d$rating)
sd(j_d$rating)

ols = lm(rating ~ ., data = j_d)
sink(file = 'results_output.txt', append = T)
summary(ols)
closeAllConnections()
