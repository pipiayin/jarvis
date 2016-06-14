#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import jieba
import jieba.posseg as pseg



from brain import Brain

class SocialBrain(Brain):


    def load(self, info):
        print("load information")

    def think(self, userSession):
        print(userSession)


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
    r = requests.get('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id='+app_id+'&client_secret='+client_secret)
    access_token = r.text.split('=')[1]
    print(access_token)
    r = requests.get('https://graph.facebook.com/v2.6/1091008854278872/subscriptions',params={'access_token':access_token})
    print(r.text)
    r = requests.get('https://graph.facebook.com/v2.6/112972272461691/friends', params={'access_token':access_token})
    print(r.text)



