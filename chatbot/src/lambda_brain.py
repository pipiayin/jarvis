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
from difflib import SequenceMatcher

from nocheckin import aws_access_key_id,aws_secret_access_key,XLineToken, happyrunXLineToken, botannXLineToken, botyunyunXLineToken, botpmXLineToken, botjhcXLineToken

lineBrain = SocialBrain()

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
lambda_client = boto3.client('lambda')

table_log = dynamodb.Table('linelog')

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

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


def responseToToken(replyToken, resp, botid=''):
#    try:
        print("to response to line replytoken")
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}


        if botid != '':
            botHeaders = getBotHeader(botid)
            if botHeaders != '':
                headers = botHeaders

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


def invokeLambdaEvent(functionName, payloadDict):
    lresponse = lambda_client.invoke(
        FunctionName = functionName,
        InvocationType ='Event',
        LogType = 'None',
        ClientContext = 'string',
        Payload = json.dumps(payloadDict),
     )


def predefineAction(msg,uid):
    msg = msg.strip()
    mapActions = [
        {'call_back':actTaipeiBus, 
         'terms':[u'幫我查公車',u'請幫我查公車',u'小姍幫我查公車', u'公車在哪裡']
        },     
        {'call_back':actLottery,
         'terms':[u'幫我抽根籤',u'請幫我抽個籤',u'小姍幫我抽簽',u'幫我抽簽看看',u'再幫我抽一次']
        }
   ]
    for a in mapActions:
       for term in a['terms']:
           if similar(term, msg) >= 0.75 or msg.startswith(term):
               return a['call_back'](msg,uid)
    return False

def actTaipeiBus(msg, uid):
    print("act TaipeiBus")
    busname = msg.strip().replace(u'幫我查公車','').replace(" ","")
    taipeiBusReq = {'uid':uid, 'busname':busname}
    invokeLambdaEvent('taipeibus', taipeiBusReq)
    return True

def actLottery(msg, uid):
    print("act Lottery")
    lotteryReq = {'uid':uid, 'botid':""}
    invokeLambdaEvent('lottery', lotteryReq)
    return True
    


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
        resp = ''
        tsid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
        bossid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
        bossmsg = u'傳下列訊息給聊天機器人 '
        dname = getUserDisplayName(fromuid)
        ts =  int(time.time())
        toLog = {'uid':fromuid, 'ts':ts, 'line':even['events'], 'msg':msg, 'resp':""}
        if 'botid' in even :
            genericBrain = GenericBrain(even['botid'],'q')
            bossid = even['bossid']
            bossNotifyList = [bossid]
            if 'bossids' in even:
                bossNotifyList = bossNotifyList + even['bossids']
            bossmsg = bossmsg + even['botid'] + " "
            resp = genericBrain.think(msg)
            notifyData = dname + bossmsg +"\n"+msg
            toLog['resp'] = resp
            toLog['botid'] = even['botid']
            table_log.put_item(Item=toLog)
            for oneBoss in bossNotifyList:
                responseToUser(oneBoss,notifyData,even['botid'])
            responseToUser(fromuid,resp,even['botid'])
        else:
            #TODO FIXME: a short cut here to invoke bus search
            didSendMsg = predefineAction(msg,fromuid)
            
            if not didSendMsg :
                resp = lineBrain.think(msg)
                toLog['resp'] = resp
                print(toLog)
                table_log.put_item(Item=toLog)
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
    predefineAction(msg, u'Uc9b95e58acb9ab8d2948f8ac1ee48fad')


    
