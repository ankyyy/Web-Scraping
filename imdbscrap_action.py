#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Author:Ankit Kumar Mishra
#Date:2nd may 2015
#Python script to extract movie info from imdb 
#input: 1.genre of movie eg.action,animation
#       2.number of pages to scrap 
#python version 2.7
#modules:1.BeautifulSoup4 
#        2.requests
#        3.pymongo
#installation command for linux 
#<apt-get install python-bs4> 
# or
#<easy_install beautifulsoup4>
# or
#<pip install beautifulsoup4>
#      
#

from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
import time
import codecs

outfile = codecs.open('main2.csv', 'w', 'utf -8')
# Genre=raw_input("Enter the genre from following \naction\nadventure\nanimation\n")
# page_no=input("No of pages to scrap")
def get_url():
    Genre="adventure"
    page_no=50
    url_new="http://www.imdb.com/search/title?genres=adventure&sort=moviemeter,asc&start=51&title_type=feature"
    url=[]
    # url.append("http://www.imdb.com/search/title?languages=hi|1&title_type=feature&sort=moviemeter,asc")
    for i in range(51,int(page_no)*50+1,50):
        url.append("http://www.imdb.com/search/title?genres=adventure&sort=moviemeter,asc&start="+str(i)+"&title_type=feature")
    return url
def get_movie_info(url):
    i=0
    client=MongoClient()
    db=client.movie_database
    movies=db.movie_collection_test
    while i<len(url):
        # print "Page no :"+str(i+1)
        # print "============================================================================="
        r  = requests.get(url[i])

        data = r.text

        soup = BeautifulSoup(data,"lxml",from_encoding="utf-8")

        try:
            for link in soup.find_all('td',attrs={'class':'title'}):
                name="not available"
                year="not available"
                outline="not available"
                rating="not available"
                runtime="not available"
                director="not available"
                movies_link="www.imdb.com"
                casts=[]
                name_obj = link.a
                year_obj = link.find('span',attrs={'class':'year_type'})
                rating_obj = link.find('span',attrs={'class':'value'})
                outline_obj = link.find('span',attrs={'class':'outline'})
                credit_obj = link.find('span',attrs={'class':'credit'})
                if credit_obj is not None:
                    dir_obj=credit_obj.find_all('a')
                    if dir_obj is not None:
                        director=dir_obj[0].text
                        for cast in dir_obj:
                            if cast is not None:
                                casts.append(cast.text)
                            else:
                                casts.append("not available")
                if len(casts) is 1:
                    continue

                genres1 = link.find('span',attrs={'class':'genre'})
                if genres1 is not None:
                    genres=genres1.find_all('a')
                else:
                    continue
                runtime_obj=link.find('span',attrs={'class':'runtime'})
                if name_obj is not None:
                    name=name_obj.text
                    movies_link=movies_link+name_obj['href']
                else:
                    continue;
                if year_obj is not None:
                    year=year_obj.text
                else:
                    continue
                if outline_obj is not None:
                    outline=outline_obj.text
                else:
                    continue
                if runtime_obj is not None:
                    runtime = runtime_obj.text
                else:
                    continue;
                if rating_obj is not None:
                    rating = rating_obj.text;
                else:
                    continue
                genre=[]
                if genres is not None:
                    for g in genres:
                        temp=g.text
                        genre.append(temp)
                else:
                    continue
                name_string=[]
                name_string=name.split(",")
                name=" ".join(name_string)
                # print "Name: "+name 
                # print "Year: "+year
                # print "Outline: "+outline
                # print "Runtime: "+runtime
                # print "Rating: "+float(str(rating))
                genre_string="-".join(genre)
                # print "Genre: "+genre_string
                # print "Director: "+director
                cast_string="-".join(casts)
                # print "Cast: "+cast_string
                outfile.write(name+"%"+year+"%"+outline+"%"+runtime+"%"+rating+"%"+genre_string+"%"+director+"%"+cast_string+"\n")
                # print "---------------------------------------------------------------------"
                # time.sleep(1)
                # print movies_link
                # new_rating=0.0
                # if rating == "not available":
                    # new_rating=0.0
                # else:
                    # new_rating=float(rating)
                # doc={"name":name,"year":year,"outline":outline,"runtime":runtime,"rating":new_rating,"genre":genre[0],"director":director}
                # movies.insert_one(doc)

        except:
            print "errorrrrrrrrrrr"
            sleep(1)
        i=i+1;
        # time.sleep(1)
    time.sleep(1)
    # print "Complete!!!"

def main():
    url=get_url()
    get_movie_info(url)


if __name__=="__main__":
    main()
