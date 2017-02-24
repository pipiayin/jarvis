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
from nocheckin import aws_access_key_id,aws_secret_access_key,XLineToken,happyrunXLineToken, botannXLineToken


dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table_log = dynamodb.Table('linelog')
table_user = dynamodb.Table('lineuser')
lambda_client = boto3.client('lambda')

learn_triggers = ['590590',u'小安 學',u'小安學']

def getLineUser(fromuid,botid=''):
    try:
        item = table_user.get_item( Key={ 'userId': fromuid })
        if "Item" in item:
            print('get user from nosql')
            print(item['Item'])
            return item['Item']

        line_url = 'https://api.line.me/v2/bot/profile/'+fromuid
        
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}
        if botid == 'happyrun':
            headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+ happyrunXLineToken}

        if botid == 'botann':
            headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+ botannXLineToken}

        print(line_url)
        r = requests.get(line_url, headers=headers)
        rjson = json.loads(r.text)
        print(rjson)
        return rjson
    except:
        print('can not line user profile from uid: '+fromuid)
        return ''


def lambda_handler(even, context):
   # try:
        print("-----get message ---")
        ts =  int(time.time())
        print(even) #
        uid = ''
        if 'userId' in even['events'][0]['source'] :
            uid = even['events'][0]['source']['userId']
        if 'groupId' in even['events'][0]['source'] :
            uid = even['events'][0]['source']['groupId']
        if 'roomId' in even['events'][0]['source'] :
            uid = even['events'][0]['source']['roomId']

        msg = even['events'][0]['message']['text']
    
        msg = msg.strip()
        toLog = {'uid':uid, 'ts':ts, 'line':even['events'], 'msg':msg}
        oneUser = getLineUser(uid)
        if 'botid' in even:
            oneUser = getLineUser(uid,even['botid'])
            oneUser['botid'] = even['botid']
            if 'botids' in oneUser:
                oneUser['botids'].append(even['botid'])
            else: 
                oneUser['botids'] = [even['botid']]

            toLog['botid'] = even['botid'] 
        if 'bossid' in even:
            oneUser['bossid'] = even['bossid']
            toLog['bossid'] = even['bossid']

        print(oneUser)
        if 'userId' in oneUser :
            table_user.put_item(Item=oneUser)
    
        print(toLog)
        table_log.put_item(Item=toLog)
        if msg.startswith(tuple(learn_triggers)) :
            print("to learn...")
            lresponse = lambda_client.invoke(
                FunctionName='ailearn',
                InvocationType='Event',
                LogType='None',
                ClientContext='string',
                Payload=json.dumps(toLog),
            )
        else:
            lresponse = lambda_client.invoke(
                FunctionName='aibrain',
                InvocationType='Event',
                LogType='None',
                ClientContext='string',
                Payload=json.dumps(even),
            )

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
            u'message': {'text':msg},
            u'botid' : 'happyrun',
            u'bossid' : 'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
           }]}

    print(lambda_handler(tmp, None))

    
