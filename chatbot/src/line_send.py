#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from __future__ import print_function 
from socialBrain import SocialBrain
import json
import boto3
import sys
import json
import time
import random
import botocore.session
import requests


XLineChannelID = ''
XLineChannelSecret = ''
XLineTrustedUserWithACL = ''

awsauthfile = 'credentials_ai'
lineauth = 'linecre.so'
with open(lineauth) as f:
    content = f.readlines()
    for line in content:
        if 'X-Line-ChannelID' in line :
            XLineChannelID = line.split("=")[1].strip()
        if 'X-Line-ChannelSecret' in line :
            XLineChannelSecret = line.split("=")[1].strip()
        if 'X-Line-Trusted-User-With-ACL' in line :
            XLineTrustedUserWithACL = line.split("=")[1].strip()


def responseToUser(uids, resp):
#    try:
        print("to response to line user")
        headers = {"Content-type": "application/json; charset=utf-8","X-Line-ChannelID" : XLineChannelID , "X-Line-ChannelSecret" : XLineChannelSecret , "X-Line-Trusted-User-With-ACL" : XLineTrustedUserWithACL}
        payload = { 
            "to":uids,
            "toChannel":1383378250,
            "eventType":"138311608800106203",
            "content":{
                "contentType":1,
                "toType":1,
                "text": resp
             }
        }  

        jdump = json.dumps(payload)
        print(jdump)
        url = 'https://trialbot-api.line.me/v1/events'
        r = requests.post(url, headers=headers, data = jdump)
        print(r)
        print(r.text)
        print("did send response")

        return ''
#    except:
#        return ''
        

def directSend(even, themsg):
   # try:
        fromuid = even['result'][0]['content']['from']
        msg = even['result'][0]['content']['text']
        responseToUser(fromuid,themsg)
        return "ok"
   # except:
   #     print(even)
   #     print(sys.exc_info()[0])
   #     return "something wrong"
   

if __name__ == '__main__':
    import sys

    #msg = sys.argv[1]
    msg = '人工智慧小姍有新版本了!還請各位有空可以跟小姍聊兩句喔 \n  --- What\'s News --- \n * 移除ptt查詢 \n * 增加知識庫 \n * 優先判斷名詞長度決定查詢 \n * 簡單過濾髒話 \n * 修改知識庫相似度參數 '

    uids=['u41b34094d1078bfd7ac91ae9a0fa2d25'] #ME
    #uids=["u0a3d105aa9f8c1ab256dffe226c1d99a", "u1ea21aa1908e6f9db4493f338add1f43", "u41b34094d1078bfd7ac91ae9a0fa2d25", "u47ea331dd00d16c830afef34795b634d", "ua112a584bffbd8898c583669931ee23b", "ubc5b714cecbad5657485548f2a6776fa", "ue38104279bcf8edf0534e038fd151006", "ueda8b2682b70f3bd7b93d72ac58a5e33", "uf234561bda4da2dd46e6486636eb607f" ,"u9c82e1183eeac7c50124d769d343657c" ]
    responseToUser(uids, msg)
    # To try from command line
    a = """tmp = {u'result': 
          [{
            u'from': u'u206d25c2ea6bd87c17655609a1c37cb8',
            u'eventType': u'138311609000106303',
                  u'content': {
                      u'from': u'u41b34094d1078bfd7ac91ae9a0fa2d25',
                      u'seq': None,
                      u'text': u'嗨嗨',
                      u'toType': 1,
                      u'to': [u'ue7f007a54c9cdc5dcd8b0dad74b4e7ad'],
                      u'location': None,
                      u'deliveredTime': 0,
                      u'createdTime': 1473144583164,
                      u'contentType': 1,
                      u'contentMetadata': {u'SKIP_BADGE_COUNT': u'true', u'AT_RECV_MODE': u'2'},
                     u'id': u'4869745949958'},
             u'to': [u'ue7f007a54c9cdc5dcd8b0dad74b4e7ad'], u'fromChannel': 1341301815, u'toChannel': 1479704687, u'createdTime': 1473144583237, u'id': u'WB1519-3801923172'}]}"""
   # print(directSend(tmp, msg))
    

    
