#-*- coding: utf-8 -*-
from pydelicious import get_popular, get_userposts, get_urlposts
import time

def initializeUserDict(tag, count=5):
    user_dict={}
    for p1 in get_popular(tag=tag)[0:count]:
        # get_urlposts()는 주어진 url에 대한 모든 게시글을 리턴
        for p2 in get_urlposts(p1['url']):
            # 리턴된 게시글들의 '유저이름'을 가져옴. '유저이름'의 value는 일단 null로 둠
            user=p2['user']
            user_dict[user]={}            
    return user_dict
    # user_dict = {'유저이름', ''}  will be returned
   
def fillItems(user_dict):
    all_items={}
    for user in user_dict:
        for i in range(3):
            try:
                # get_userposts()는 주어진 사용자에 대한 모든 게시글을 리턴
                posts=get_userposts(user)
                break
            except:
                print "Failed user "+user+", retrying"
                time.sleep(4)
                
        for post in posts:
            url=post['url']
            user_dict[user][url]=1.0
            all_items[url]=1
            # user_dict = {'유저이름', {'url 주소' : 평가점수1 or 0}}  will be returned
            # all_items = { 'url주소' : 1}
            
    #참조 list(d.items()) == list(zip(d.keys(), d.values()))
    # user_dict.values()는 '유저이름'을 를 가리킴
    for ratings in user_dict.values():
        for item in all_items:
            if item not in ratings:
                ratings[item]=0.0
                
    
    # tag='programming'으로 검색시 1st user 값이 ''임. 에러남. 다른 쿼리를 날리니 괜찮아졌으나 fillItems 할 때 요청/응답받는 데이터량이 너무 많음
    
            
