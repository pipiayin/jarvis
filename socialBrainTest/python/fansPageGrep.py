#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import random
import sys
import time

access_token = ''


def getResponse(path, params={}):
    params['access_token'] = access_token
    r = requests.get('https://graph.facebook.com/v2.6/'+path,params=params)
    return json.loads(r.text)

def grepUser(cuser,params={}):
    params['access_token'] = access_token
    oneUser = getResponse('/'+cuser, params)
    print(oneUser)
    bucket.upsert(oneUser['id'],oneUser)

def grepPost(cuser,params={}):
    params['access_token'] = access_token
    oneUser = getResponse('/'+cuser, params)
    print(oneUser)
    bucket.upsert(oneUser['id'],oneUser)

if __name__ == '__main__':

    s = open('secret.so')
    client_secret= s.readline().strip()
    s.close()

    app_id = '1091008854278872'
#    app_id = '397433603789585'
    fb_page= 'WuXianZhuiXingYanJiuSuo'

    r = requests.get('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id='+app_id+'&client_secret='+client_secret)
    print(r.text)
    access_token = json.loads(r.text)['access_token']
    print(access_token)
    params_user={'fields':'id,about,bio,name,link'}
    print("====== handle all user =======")
    
    #user_token = 'EAAPgREs0wtgBAJ2MmLu4RvfnZBsKZAhyZB1yjUgtkDJcNuZBGzXHdwcWn7HgbtZBPfW9ES9zcWVFLOWKCxZAhyqhs1skclGpWyLRMvpZCjxE9MEjZAjPDDDZAPZAhlFp2wMTRH8rFwxNPAF6mNR5THhveLRlzoKPIw2KZAFMfCaiUJ2jUi7CD9VXRHR'
    r = getResponse(fb_page,params={'access_token':access_token, 'type':'page'})

    print(r)
    page_id = r['id']
    r = getResponse(page_id+"/posts",params={'access_token':access_token, 'type':'post'})

    cnt = 1
    for i in r['data']:
        print(i)
        cnt += 1
        if cnt >= 5:
            break
