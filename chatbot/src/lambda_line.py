#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from __future__ import print_function 
import json
import boto3
import sys
import json
import time
import random
import botocore.session
import requests
from lineTools import getBotHeader
from nocheckin import aws_access_key_id,aws_secret_access_key,XLineToken,bossid
from blackList import badfriends


dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table_log = dynamodb.Table('linelog')
table_user = dynamodb.Table('lineuser')
lambda_client = boto3.client('lambda')

learn_triggers = ['590590',u'小安 學',u'小安學']
group_triggers = [u'小姍',u'小安','JHC']



def lineResponse(toLineResponse):
    lresponse = lambda_client.invoke(
         FunctionName='lineResponse',
         InvocationType='Event',
         LogType='None',
         ClientContext='string',
         Payload=json.dumps(toLineResponse),
    )

def getLineUser(fromuid,botid=''):
    try:
        item = table_user.get_item( Key={ 'userId': fromuid })
#        if "Item" in item:
#            print('get user from nosql')
#            print(item['Item'])
 

        line_url = 'https://api.line.me/v2/bot/profile/'+fromuid
        
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}

        if botid != '':
            botHeaders = getBotHeader(botid)
            if botHeaders != '':
                headers = botHeaders
            print(headers)

        print(line_url)
        r = requests.get(line_url, headers=headers)
        rjson = json.loads(r.text)
        print(rjson)
        return rjson
    except:
        print('can not line user profile from uid: '+fromuid)
        return ''

def invoke_lambda_event(functionName, payload):
    lresponse = lambda_client.invoke(
        FunctionName = functionName,
        InvocationType = 'Event',
        LogType = 'None',
        ClientContext = 'string',
        Payload = payload
    )
    return lresponse


def lambda_handler(even, context):
   # try:
        print("-----get message from lambda line---")
        ts =  int(time.time())
        print(even) #
        uid = ''
        #bossid = 'Uc9b95e58acb9ab8d2948f8ac1ee48fad', bossid from import nocheckin, I know it is a bad design but...
        isGroup = False
        if 'userId' in even['events'][0]['source'] :
            uid = even['events'][0]['source']['userId']
        if 'groupId' in even['events'][0]['source'] :
            isGroup = True
            uid = even['events'][0]['source']['groupId']
        if 'roomId' in even['events'][0]['source'] :
            isGroup = True
            uid = even['events'][0]['source']['roomId']

        msg = '_'
        messageType = 'text'

        if 'text' == even['events'][0]['message']['type']:
            msg = even['events'][0]['message']['text']

        if 'image' == even['events'][0]['message']['type']:
            if uid in badfriends:
                msg = '抱歉 目前系統認定是你是壞朋友 你送的圖就先不理會了 如果要申訴 請email給我主人: ai@talent-service.com'
                toLineResponse = {'uid':uid, 'msg':msg}
                lineResponse(toLineResponse)
                toLineResponse = {'uid':bossid, 'msg': "有人傳圖片被擋:"+uid}
                lineResponse(toLineResponse)

                return

            messageType = 'image'
            imageId = even['events'][0]['message']['id']
            imageAnalysis = {'uid':uid, 'imageId': imageId}

            invoke_lambda_event('facerecognize', json.dumps(imageAnalysis) )

        even['isGroup'] =  str(isGroup) 
        msg = msg.strip()
        toLog = {'uid':uid, 'ts':ts, 'line':even['events'], 'msg':msg, 'isGroup': str(isGroup)}
        oneUser = getLineUser(uid)
        if 'botid' in even:
            oneUser = getLineUser(uid,even['botid'])
            oneUser['botid'] = even['botid']
            if 'botids' in oneUser:
                if even['botid'] not in oneUser['botids']:
                    oneUser['botids'].append(even['botid'])
            else: 
                oneUser['botids'] = [even['botid']]

            toLog['botid'] = even['botid'] 
        if 'bossid' in even:
            oneUser['bossid'] = even['bossid']
            toLog['bossid'] = even['bossid']
        if 'bossids' in even:
            oneUser['bossids'] = even['bossids']
            toLog['bossids'] = even['bossids']

        oneUser['last'] = ts
        if 'state' not in oneUser:
            oneUser['state'] = 'chatting'

        print(oneUser)
        if 'userId' in oneUser :
            table_user.put_item(Item=oneUser)
    
        print(toLog)
   
        table_log.put_item(Item=toLog)
        if messageType == 'image':
            return "imageOk"

        if msg.startswith(tuple(learn_triggers)) :
            if isGroup:
                print("ignore learn from group")
            else: 
                print("to learn")
                invoke_lambda_event('ailearn', json.dumps(toLog) )
        else:
            print("to trigger ai brain \n\n")
            if isGroup :
                if msg.startswith(tuple(group_triggers)):
                    print("in group trigger")
                    tmpmsg = msg
                    for t in group_triggers:
                        tmpmsg = tmpmsg.replace(t,'')

                    even['events'][0]['message']['text'] = tmpmsg
                    invoke_lambda_event('ailearn', json.dumps(even) )
            else:
                print('not group...')
                invoke_lambda_event('aibrain', json.dumps(even) )

        print("responsed (tolog->)"+str(toLog))
        return "ok"
   # except:
        print(even)
        print(sys.exc_info()[0])
        return "something wrong"
   

if __name__ == '__main__':
    import sys

    msg = sys.argv[1]

    # To try from command line
    tmp = {u'events':
          [{
            u'source': {'userId': u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'},
            #u'message': { 'type':'image' , 'id':'6435322417921'},
            u'message': { 'type':'text' , 'text':msg},
            u'bossid' : 'Uc9b95e58acb9ab8d2948f8ac1ee48fad',
           }]}

    print(lambda_handler(tmp, None))

    
