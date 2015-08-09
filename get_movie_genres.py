import csv, json, os, requests
from time import sleep
import pandas as pd

#set directory
os.chdir("C:/Users/Matt/Dropbox/github/scrapes/temp/")

#create dictionary to hold results
dict = {}

#pull in list of movies
films = []
with open('filmjunk_ratings.csv', 'rU') as csvfile:
    read = csv.reader(csvfile, delimiter = '\t')  
    
    for row in read:
        films.append(row[0])
        
films.remove('movie')

films = list(set(films))


for film in films:
    
    try:
    
        sleep(1)    
    
        #create sub-dictionary
        dict[film] = {}
    
        #format movie string for url
        movie = film.lower().split()
        movie = '+'.join(movie)
        
        url = 'http://www.omdbapi.com/?t=' + movie + '&y=&plot=short&r=json'
        
        r = requests.get(url)
        parsed_json = json.loads(r.text)
        
        genres = parsed_json['Genre']
    
        genres = genres.split(', ')

        #add to dictionary
        for num_genre in range(0, len(genres)):
            dict[film]['genre_' + str(num_genre)] = genres[num_genre]
   
    except:
        pass

  
#create dateframe from dictionary
df = pd.DataFrame([[col1,col2] for col1, d in dict.items() for col2 in d.values()])
      
df.columns = ['movie', 'genre']

#write ratings to csv
rows = zip(list(df.movie), list(df.genre))

with open('movie_genres.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = '\t')
    writer.writerow(('movie', 'genre'))

    for row in rows:
        writer.writerow(row)                  
                                 
                                          
                                                   
                                                            
                                                                     
                                                                                       


 
    






