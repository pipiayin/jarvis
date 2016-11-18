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

lineBrain = SocialBrain()

XLineChannelID = ''
XLineChannelSecret = ''
XLineTrustedUserWithACL = ''
XLineToken=''

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
        if 'X-Line-ChannelAccessToken' in line :
            XLineToken = line.split(" =")[1].strip()


def responseToUser(uid, resp):
#    try:
        print("to response to line user")
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}
        #headers = {"Content-type": "application/json; charset=utf-8","X-Line-ChannelID" : XLineChannelID , "X-Line-ChannelSecret" : XLineChannelSecret , "X-Line-Trusted-User-With-ACL" : XLineTrustedUserWithACL}
        payload = { 
            "to": uid ,
            "messages":[{
                "type":"text",
                "text": resp
             }]
        }  

        jdump = json.dumps(payload)
        print(jdump)
        url = 'https://api.line.me/v2/bot/message/push'
        #url = 'https://trialbot-api.line.me/v1/events'
        r = requests.post(url, headers=headers, data = jdump)
        print(r.text)
        print("did send response")

        return ''
#    except:
#        return ''
        

def getUserDisplayName(fromuid):
    try:
        line_url = 'https://api.line.me/v2/bot/profile/'+fromuid
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}

        r = requests.get(line_url, headers=headers)
        rjson = json.loads(r.text)
        ruser = rjson['displayName']
        return ruser
    except:
        print('can not get displayName from uid:'+fromuid)
        return ''

def lambda_handler(even, context):
   # try:
        print("-----get message this is lambda brain ---")
        fromuid = even['events'][0]['source']['userId']
        msg = even['events'][0]['message']['text']
        resp = lineBrain.think(msg)
        responseToUser(fromuid,resp)

        dname = getUserDisplayName(fromuid)
        notifyData = dname +" 傳下列訊息給小姍:\n"+msg
        meid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
        responseToUser(meid,notifyData)
        return "ok"
   # except:
   #     print(even)
   #     print(sys.exc_info()[0])
   #     return "something wrong"
   

if __name__ == '__main__':
    import sys

    msg = sys.argv[1]

    # To try from command line
    tmp = {u'events': 
          [{
            u'source': {'userId': u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'},
            u'message': {'text':u'test test test test'}
           }]}   
    print(lambda_handler(tmp, None))

    
