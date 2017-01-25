#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from __future__ import print_function 
from socialBrain import SocialBrain, GenericBrain

import json
import boto3
import sys
import json
import time
import random
import botocore.session
import requests
from nocheckin import aws_access_key_id,aws_secret_access_key,XLineToken, happyrunXLineToken

lineBrain = SocialBrain()


def responseToToken(replyToken, resp, botid=''):
#    try:
        print("to response to line replytoken")
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}
        if botid == 'happyrun' :
            headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+ happyrunXLineToken}
        payload = { 
            "replyToken": replyToken ,
            "messages":[{
                "type":"text",
                "text": resp
             }]
        }  

        jdump = json.dumps(payload)
        print(jdump)
        url = 'https://api.line.me/v2/bot/message/reply'
        #url = 'https://trialbot-api.line.me/v1/events'
        r = requests.post(url, headers=headers, data = jdump)
        print(r.text)
        print("did send response")
        return ''

def responseToUser(uid, resp, botid=''):
#    try:
        print("to response to line user")
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}
        if botid == 'happyrun' :
            headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+ happyrunXLineToken}
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
        

def getUserDisplayName(fromuid, botid=''):
    try:
        line_url = 'https://api.line.me/v2/bot/profile/'+fromuid
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}

        if botid == 'happyrun' :
            headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+ happyrunXLineToken}
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
        fromuid = ''
        if 'userId' in even['events'][0]['source'] :
            fromuid = even['events'][0]['source']['userId']
        if 'groupId' in even['events'][0]['source'] :
            fromuid = even['events'][0]['source']['groupId']
            print("---- the fromuid is actual groupId")
        if 'roomId' in even['events'][0]['source'] :
            fromuid = even['events'][0]['source']['roomId']
            print("---- the fromuid is actual roomId")

        msg = even['events'][0]['message']['text']
        replyToken = even['events'][0]['replyToken']
        resp = ''
        tsid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
        bossid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
        bossmsg = u'傳下列訊息給聊天機器人 '
        dname = getUserDisplayName(fromuid)
        if 'botid' in even :
            genericBrain = GenericBrain(even['botid'],'q')
            bossid = even['bossid']
            bossmsg = bossmsg + even['botid'] + " "
            resp = genericBrain.think(msg)
            notifyData = dname + bossmsg +"\n"+msg
            responseToUser(bossid,notifyData)
            responseToUser(fromuid,resp)
            #responseToToken(replyToken,resp,even['botid'])
        else:
            resp = lineBrain.think(msg)
            #responseToToken(replyToken,resp)
            responseToUser(fromuid,resp)

        notifyData = dname + bossmsg +"\n"+msg
        responseToUser(tsid,notifyData)
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
            u'message': {'text':msg}
           }]}   
    print(lambda_handler(tmp, None))

    
