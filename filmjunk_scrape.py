from bs4 import BeautifulSoup
from time import sleep
import csv, os, re, requests
from rating_clean import rating_clean 
import pandas as pd

#set directory
os.chdir("C:/Users/Matt/Dropbox/github/scrapes/temp/")

#create dictionary to hold movie ratings by host
dict = {}

webpages = ['http://filmjunk.com/podcast/',
            'http://filmjunk.com/podcast-archives-14/',
            'http://filmjunk.com/podcast-archives-13/',
            'http://filmjunk.com/podcast-archives-12/',
            'http://filmjunk.com/podcast-archives-11/',
            'http://filmjunk.com/podcast-archives-10/']

for webpage in webpages:

    sleep(1.01)    
    
    #get webpage
    web_page = requests.get(webpage)
    
    
    #create beautifulsoup object
    soup = BeautifulSoup(web_page.content)
    
    #define raters to search for
    raters = ['Jay', 'Sean', 'Frank']
    
    #find paragraph with movie title and host ratings
    for tag in soup.find_all('p'):
    
        try:
            if len(tag.next_element.contents) >= 1:
                header = tag.next_element.contents[0]
        
                if header == 'Reviews':                #found Review paragraph

                    movies = []
                    
                    #grab all movies reviewed that week
                    for movie_link in tag.find_all('a'):
                        movies.append(movie_link.contents[0].encode('utf-8'))

                    for movie in movies:
            
                        dict[movie] = {}                   #create dict to hold raters/reviews
                
                        for rater in raters:
                    
                            #find rater within paragraph
                            result = tag.find(text = re.compile('.\s*' + rater + ':\s*'))
                
                            #find star image and extract url
                            star = result.next_element.get('src')
        
                            dict[movie][rater] = {}
    
                            #add rating value
                            dict[movie][rater]['rating'] = rating_clean(star.encode('utf-8'))[0]
    
                            #add star system value
                            dict[movie][rater]['system'] = rating_clean(star.encode('utf-8'))[1]
                    
    
        except AttributeError:
            pass
    


#create dateframe from dictionary
df = pd.DataFrame([[col1,col2,col3,col4] for col1, d in dict.items() for col2, e in d.items() for col3, col4 in e.items()])

df.columns = ['movie', 'rater', 'key', 'value']

#write ratings to csv
rows = zip(list(df.movie), list(df.rater), list(df.key), list(df.value))

with open('filmjunk_ratings.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = '\t')
    writer.writerow(('movie', 'rater', 'key', 'value'))

    for row in rows:
        writer.writerow(row)



