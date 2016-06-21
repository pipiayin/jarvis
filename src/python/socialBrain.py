#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import jieba
import jieba.posseg as pseg
import random
import time


 
access_token = ''
from brain import Brain

class SocialBrain(Brain):


    def load(self, info):
        print("load information")

    def think(self, userSession):
        print(userSession)



def getResponse(path, params={}):
    params['access_token'] = access_token
    r = requests.get('https://graph.facebook.com/v2.6/'+path,params=params)
    return json.loads(r.text)

def getTagFriend(cuser):
    tag_friend_list = getResponse('/'+cuser+"/taggable_friends", params)
    print("=== taggable friends")
    print(tag_friend_list)
    print("=== taggable friends end ")


if __name__ == '__main__':

    fbBrain = SocialBrain()
    
    jieba.set_dictionary('data/dict.txt.big')

    s = open('secret.so')
    client_secret= s.readline().strip()
    s.close()

    userSession = {"name":"","lastWords":"", "lastString":""}
    userReq = u'照片不錯'
    words = pseg.cut(userReq)
    userSession["lastWords"]  = words
    userSession["lastString"]  = userReq

    fbBrain.think(userSession)

    app_id = '1091008854278872'
#    app_id = '397433603789585'

    r = requests.get('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id='+app_id+'&client_secret='+client_secret)
    print(r.text)
    access_token = r.text.split('=')[1]
    print(access_token)
    
    #r = requests.get('https://graph.facebook.com/v2.6/'+app_id+'/subscriptions',params={'access_token':access_token})
    #print(r.text)
#    r = getResponse('https://graph.facebook.com/v2.6/'+app_id+'/connections',params={'access_token':access_token})
#    print(r)
    #print(r.text)
    #r = getResponse('/'+app_id+'/accounts/test-users',params={'access_token':access_token})
    #print(r.text)
    user_token = 'EAAPgREs0wtgBAJ2MmLu4RvfnZBsKZAhyZB1yjUgtkDJcNuZBGzXHdwcWn7HgbtZBPfW9ES9zcWVFLOWKCxZAhyqhs1skclGpWyLRMvpZCjxE9MEjZAjPDDDZAPZAhlFp2wMTRH8rFwxNPAF6mNR5THhveLRlzoKPIw2KZAFMfCaiUJ2jUi7CD9VXRHR'
    r = getResponse('search',params={'access_token':access_token,'q':u'育兒', 'type':'page'})
    handle_user_list=[]
    for item in r['data']:
        print(item)
        page_id = item['id']
        pager = getResponse("/"+page_id+"/posts")
#        print(pager)
        for post in pager['data']:
            time.sleep(random.randint(2, 3))
            print(post['id']) 
            params={'fields':'id,from,message'}
            postDetail = getResponse('/'+post['id'],params)
            if ('message' in postDetail) and (len(postDetail['message']) <= 30) :
                print(postDetail)
            else:
                print("message is too long or no message..."+ str(postDetail['from']))
            cuser = postDetail['from']['id']
            if handle_user_list.count(cuser) == 0:
                handle_user_list.append(cuser)
          #      getTagFriend(cuser)

            comments = getResponse('/'+post['id']+"/comments",params)
            print('------comments start---')
            for comment in comments['data']:
                cuser = comment['from']['id']
                if handle_user_list.count(cuser) == 0:
                    handle_user_list.append(cuser)
                 #   getTagFriend(cuser)
                     
            print('------comments end---')
    

    print("====== all handled =======")
    print(handle_user_list)
    for u in handle_user_list:
        uprofile = getResponse('/'+u, params={'access_token':access_token})
        print(uprofile)
        uposts = getResponse("/"+u+"/posts", params={'access_token':access_token})
        print(uposts)
        for upost in uposts:
            print(upost)
       



