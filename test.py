#!/usr/bin/env python
# -*- coding: latin-1 -*-

#Author:Ankit kumar mishra
#Date:2nd may 2015
#Python script to extract movie info from imdb 

from bs4 import BeautifulSoup
import requests
import time
import codecs
#########################################################################################################################
outfile = codecs.open('main.csv', 'a', 'utf -8')
def get_url():
    Genre="action"
    url=[]
    url.append("http://www.imdb.com/search/title?genres="+Genre+"&title_type=feature&sort=moviemeter,asc")
    for i in range(51,int(25)*50+1,50):
        url.append("http://www.imdb.com/search/title?genres="+Genre+"&sort=moviemeter,asc&start="+str(i)+"&title_type=feature")
    return url
############################################# get top 250 movies links ########################################################
def get_top250_links():
    r  = requests.get("http://www.imdb.com/chart/top")

    data = r.text

    soup = BeautifulSoup(data,"lxml",from_encoding="utf-8")
    movie_list=[]
    try:
        for link in soup.find_all('td',attrs={'class':'titleColumn'}):
            movies_link=None
            name_obj = link.a
            if name_obj is not None:
                movies_link=name_obj['href'][0:17]
            if movies_link is not None:
                movie_list.append(movies_link)
                # print movies_link
    except:
        print "errorrrrrrrrrrr"
        sleep(1)
    return movie_list
 ############################ get action movies links ###############################################################################       
def get_movie_links(url):
    i=0
    movie_list=[]
    while i<len(url):
        r  = requests.get(url[i])

        data = r.text

        soup = BeautifulSoup(data,"lxml",from_encoding="utf-8")

        try:
            for link in soup.find_all('td',attrs={'class':'title'}):
                movies_link=None
                name_obj = link.a
                if name_obj is not None:
                    movies_link=name_obj['href']
                if movies_link is not None:
                    movie_list.append(movies_link)
                    # print movies_link
        except:
            print "errorrrrrrrrrrr"
            sleep(1)
        i=i+1;
    return movie_list
#########################################################################################################################
def get_ratings(movie_list):
    print len(movie_list)
    index=0
    while index<len(movie_list):
        print index+1
        for page_no in range(0,40,10):
            r  = requests.get("http://www.imdb.com"+str(movie_list[index])+"reviews?start="+str(page_no))
            # r =  requests.get("http://www.imdb.com"+list(movie_list)[index]+"reviews?ref_=tt_ov_rt")

            data = r.text
            soup = BeautifulSoup(data)
            title= soup.title.text.split()
            title=title[0:len(title)-5]
            # print "page - "+ str(page_no/10)
            list_obj = soup.find_all('img',attrs={"width":"102","height":"12"})
            # print len(list_obj)
            if len(list_obj):
                try:
                    for link in list_obj:
                        temp=link['alt'].split('/')
                        rating = float(float(temp[0])/float(10))
                        user_obj = link.next.next.next.next.next.next
                        user_id = user_obj['href']
                        # print user_id[8:len(user_id)-1]+","+" ".join(title)+","+str(rating)
                        outfile.write(user_id[8:len(user_id)-1]+","+" ".join(title)+","+str(rating)+"\n")
                except:
                    # sleep(1)
                    print "errorrrrrrrrrrr"
                    pass
            else:
                break
        index=index+1

def main():
    url=get_url()
    movie_list=get_movie_links(url)
    # movie_list_top250 = get_top250_links()
    get_ratings(movie_list)
    
if __name__ == "__main__":
    main()
