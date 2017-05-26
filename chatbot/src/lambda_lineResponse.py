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
from nocheckin import aws_access_key_id,aws_secret_access_key,XLineToken, happyrunXLineToken, botannXLineToken, botyunyunXLineToken, botpmXLineToken, botjhcXLineToken


def getBotHeader(botid):
    botMap = {'happyrun':happyrunXLineToken,
              'botann':botannXLineToken,
              'botpm':botpmXLineToken,
              'botjhc':botjhcXLineToken,
              'botyunyun':botyunyunXLineToken}
    if botid in botMap:
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+botMap[botid]}
        return headers
    else:
        return ""

def getUserDisplayName(fromuid, botid=''):
    try:
        line_url = 'https://api.line.me/v2/bot/profile/'+fromuid
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}

        if botid != '':
            botHeaders = getBotHeader(botid)
            if botHeaders != '':
                headers = botHeaders

        r = requests.get(line_url, headers=headers)
        rjson = json.loads(r.text)
        ruser = rjson['displayName']
        return ruser
    except:
        print('can not get displayName from uid:'+fromuid)
        return ''



def responseToUser(uid, resp, botid=''):
#    try:
        print("to response to line user, with botid:"+botid+"-end-")
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}


        if botid != '':
            botHeaders = getBotHeader(botid)
            if botHeaders != '':
                headers = botHeaders

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
        print("----headers---")
        print(headers)
        r = requests.post(url, headers=headers, data = jdump)
        print(r.text)
        print("did send response")

        return ''
#    except:
#        return ''
        


def lambda_handler(even, context):
   # try:
        print("-----just response message to a uid ---")
        # all we need in even{} is uid, msg, botid
        botid = ''
        if 'uid' in even and 'msg' in even:
            if 'botid' in even: 
                botid = even['botid']
        else:
            return

        responseToUser(even['uid'],even['msg'],botid)

        tsid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
        bossid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
        bossmsg = u'聊天機器人回傳訊息使用者 '
        dname = getUserDisplayName(even['uid'])
        ts =  int(time.time())
        if 'botid' in even :
            notifyData = dname + bossmsg +"\n"+ even['msg']
            for oneBoss in bossNotifyList:
                responseToUser(oneBoss,notifyData,even['botid'])
            #responseToToken(replyToken,resp,even['botid'])
        return
   # except:
   #     print(even)
   #     print(sys.exc_info()[0])
   #     return "something wrong"
   

if __name__ == '__main__':
    import sys

    # To try from command line
    tmp={'uid':u'Uc9b95e58acb9ab8d2948f8ac1ee48fad','msg':'a short url'}
    print(lambda_handler(tmp, None))

    
