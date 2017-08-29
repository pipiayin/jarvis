#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from __future__ import print_function 
import json
import boto3
import sys
import datetime
import json
import time
import random
import botocore.session
import requests
from lineTools import getBotHeader
from nocheckin import aws_access_key_id,aws_secret_access_key,XLineToken,bossid
from blackList import badfriends
import decimal


dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table_user = dynamodb.Table('lineuser')
lambda_client = boto3.client('lambda')

learn_triggers = ['590590',u'小安 學',u'小安學']
group_triggers = [u'小姍',u'小安','JHC']



def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj)
    raise TypeError

def lineResponse(toLineResponse):
    lresponse = lambda_client.invoke(
         FunctionName='lineResponse',
         InvocationType='Event',
         LogType='None',
         ClientContext='string',
         Payload=json.dumps(toLineResponse),
    )

def getLineUser(fromuid,botid=''):
#    try:
        item = table_user.get_item( Key={ 'userId': fromuid })
        oneUser = {}
        n = datetime.datetime.now().timestamp()
        if "Item" in item:
            print('get user from nosql')
            #print(item['Item'])
#            return item['Item']
            oneUser = item['Item']
            if 'profile' not in oneUser:
                oneUser['profile'] = {}
        else:
            oneUser['last'] = 0
            oneUser['created'] = int(n)
            oneUser['profile'] = {}
            print("this is new user!!! userId="+fromuid)

        if (n - int(oneUser['last'])) <= 60*60*24:
            print("do not update Line profile in 24 hours")
            return oneUser

        line_url = 'https://api.line.me/v2/bot/profile/'+fromuid
        
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}

        if botid != '':
            botHeaders = getBotHeader(botid)
            if botHeaders != '':
                headers = botHeaders

        r = requests.get(line_url, headers=headers)
        rjson = json.loads(r.text)
        print(rjson)
        if 'message' in rjson and rjson['message'] == 'Not found':
            return oneUser

        print("do the update oneUser")
        if 'pictureUrl' in rjson:
            oneUser['pictureUrl'] = rjson['pictureUrl']
        else:
            oneUser['pictureUrl'] = 'none'
        oneUser['displayName'] = rjson['displayName']
        if 'profile' not in oneUser:
            oneUser['profile'] = {}
        oneUser['profile']['name'] = rjson['displayName']
        oneUser['userId'] = rjson['userId']
        return oneUser
#    except:
#        print('exception for get user profile from uid: '+fromuid)
#        return ''

def invoke_lambda_event(functionName, payload):
    lresponse = lambda_client.invoke(
        FunctionName = functionName,
        InvocationType = 'Event',
        LogType = 'None',
        ClientContext = 'string',
        Payload = payload
    )
    return lresponse


def sendDeny(uid, bossid, msg):
    toLineResponse = {'uid':uid, 'msg':msg}
    lineResponse(toLineResponse)
    toLineResponse = {'uid':bossid, 'msg': msg+"->"+uid}
    lineResponse(toLineResponse)


def isAllowImage(oneUser):
    if 'profile' in oneUser and 'allow' in oneUser['profile'] and 'image' in oneUser['profile']['allow'] :
        return True
    return False

def setAllowImage(oneUser):
    print('do dynamodb update user to allow image analysis')
    if 'profile' not in oneUser:
        oneUser['profile'] = {}

    if 'allow' not in oneUser['profile']:
        oneUser['profile']['allow'] = []

    if 'image' not in oneUser['profile']['allow']:
        oneUser['profile']['allow'].append('image')
    
    table_user.put_item(Item=oneUser)

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
        oneUser = {}
        oneUser = getLineUser(uid)

        if 'state' in oneUser and oneUser['state'] == 'prohibit':
            msg = '人工智慧分析過去聊天記錄 認定是你是壞朋友 目前小姍不願意和你聊天 如果要申訴 請email至: ai@talent-service.com'
            sendDeny(uid,bossid,msg)
            return

        if 'text' == even['events'][0]['message']['type']:
            msg = even['events'][0]['message']['text']
        if 'sticker' == even['events'][0]['message']['type']:
            packageId = even['events'][0]['message']['packageId']
            if packageId == '1540679':
                msg = '大感謝~ 幫忙買了小姍貼圖~ 照片分析功能開啟!'
                setAllowImage(oneUser)
                sendDeny(uid,bossid,msg)

        if 'image' == even['events'][0]['message']['type']:
            if uid in badfriends:
                msg = '抱歉 目前系統認定是你是壞朋友 你送的圖就先不理會了 如果要申訴 請email給我主人: ai@talent-service.com'
                sendDeny(uid,bossid,msg)
                return

            if isGroup:
                msg = '抱歉 小姍最近看圖兼分析實在太累了 在群組中送的圖就先不理會了 但是個別好友送圖來給我 我還是會努力的看用力地看唷...如果要申訴 請email給我主人: ai@talent-service.com'
                sendDeny(uid, bossid, msg)
                return

            imageId = even['events'][0]['message']['id']
            msg = uid + "_" + imageId

            if isAllowImage(oneUser):
                messageType = 'image'
                imageAnalysis = {'uid':uid, 'imageId': imageId}
                invoke_lambda_event('facerecognize', json.dumps(imageAnalysis) )
            else:
                msg = '小姍最近訊息太多，又要看照片分析，快累到不行了:~~ \n 目前先開放購買小姍貼圖的好友分析照片...(買了小姍的日常貼圖後 傳任一張給小姍看一下) 感恩啦~ '
                sendDeny(uid, bossid, msg)
                msg = uid + "_" + imageId

        even['isGroup'] =  str(isGroup) 
        msg = msg.strip()
        toLog = {'uid':uid, 'ts':ts, 'line':even['events'], 'msg':msg, 'isGroup': str(isGroup)}
        #oneUser = getLineUser(uid)
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

        if 'state' not in oneUser:
            oneUser['state'] = 'chatting'
        if 'history' not in oneUser:
            oneUser['history'] = [msg]
        else:
            oneUser['history'].append(msg)

        if len(oneUser['history']) > 51:
            oneUser['history'].remove(oneUser['history'][0])

       # if len(oneUser['history']) >= 5  and len(set(oneUser['history'][-5:]))==1:
       #     print("handle repeating")
       #     msg = '請冷靜 你好像在講重複的話'
       #     toLineResponse = {'uid':uid, 'msg':msg}
       #     lineResponse(toLineResponse)
       #     toLineResponse = {'uid':bossid, 'msg': msg+":"+uid+":"+oneUser['displayName']}
       #     lineResponse(toLineResponse)
       #     return


        print(oneUser)
        if 'created' not in oneUser :
            oneUser['created'] = 0
            if 'last' not in oneUser:
            # that means new users after created colume built
                oneUser['created'] = ts

        oneUser['last'] = ts
        even['oneUser'] = oneUser
        if 'userId' in oneUser :
            print('do dynamodb update user')
            table_user.put_item(Item=oneUser)
    
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
                    print('message to aibrain')
                    print(json.dumps(even,default=decimal_default))
                    invoke_lambda_event('aibrain', json.dumps(even,default=decimal_default) )
            else:
                print('not group...')
                invoke_lambda_event('aibrain', json.dumps(even,default=decimal_default) )

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
            #u'source': {'groupId': u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'},
            #u'message': { 'type':'image' , 'id':'6435322417921'},
            u'message': { 'type':'text' , 'text':msg},
            #u'message': {u'type': u'sticker', u'id': u'6475887180969', u'packageId': u'3524', u'stickerId': u'2713770'},
           
            u'bossid' : 'Uc9b95e58acb9ab8d2948f8ac1ee48fad',
           }]}

    tmp = {'events':[{'type': 'message', 'replyToken': '4e184e77a33841d0ae95c8bf4b8dd300', 'source': {'userId': 'Uc9b95e58acb9ab8d2948f8ac1ee48fad', 'type': 'user'}, 'timestamp': 1503969668255, 'message': {'type': 'sticker', 'id': '6614883524485', 'stickerId': '19099990', 'packageId': '1540679'}}]}
    print(lambda_handler(tmp, None))

    
