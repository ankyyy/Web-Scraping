#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup

import requests


r  = requests.get("http://www.imdb.com/title/tt1386697/reviews?start=0")

data = r.text

soup = BeautifulSoup(data)
list_obj = soup.find_all('img',attrs={"width":"102","height":"12"})
# print len(list_obj)
if len(list_obj):
    try:
        for link in list_obj:
            # num_rating =  link['alt']
            print link['alt']
            # value = int(rating[0])/int(rating[2])
            # rating = float(float(num_rating[0])/float(10))

            user_obj = link.next.next.next.next.next.next
            user_id = user_obj['href']
            print user_id
            # print user_id[8:len(user_id)-1]+","+title+","+str(rating)
    except:
        print "errorrrrrrrrrrr"
         # index=index+1
        pass
else:
    print "empty"

# try:
#     for link in soup.find_all('td'):
#          if  link.get('class')[0]== 'titleColumn':
# 		 # for child in link.descendants:
#   		 	# print child.string
# 		# print link.a.has_attr('href') 
# 		 for item in link.find_all('span',attrs={'class':'secondaryInfo'}):
# 			if item is not None:
# 				print item.next_element   
# 		 #a=link.find('a')
#                  #name=a.get_text()
#                  #temp=link.next_sibling
#                  #rating=temp.next_sibling.strong.text
#                  #temp2=link.span.next_sibling.next_sibling.next_sibling.next_sibling   
#                  #year=temp2.text    
#                  #print name+","+rating+","+year
        
# except:
#     pass
