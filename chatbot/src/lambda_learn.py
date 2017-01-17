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

from elasticsearch import Elasticsearch, RequestsHttpConnection
from datetime import datetime
from requests_aws4auth import AWS4Auth
from awsconfig import ESHOST, REGION
from nocheckin import aws_access_key_id,aws_secret_access_key,XLineToken,happyrunXLineToken
from blackList import badfriends,badwords

min_score=1.5

#host = 'search-sandyai-mdmcmay32zf36sgmk66tz2v454.us-east-1.es.amazonaws.com'
host = ESHOST
region = REGION

bossid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'

awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, region, 'es')

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)


learn_trigger = '590590'

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


def responseToUser(uid, resp, botid=''):
#    try:
        print("to response to line user")
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}

        if botid =='happyrun':
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
        r = requests.post(url, headers=headers, data = jdump)


def lambda_handler(even, context):
    try:
        print("-----learn from message ---")
        msg = even['msg'].strip()
        fullmsg = msg
        print(even)
        botid = ''
        indexname = 'testi'
        if 'botid' in even :
            botid = even['botid']
            indexname = botid

        if not msg.startswith(learn_trigger):
            print('should not learn things here !!')
            print(msg)
            return ''
        msg = msg.replace(learn_trigger,'')
        msg = msg.strip()
        parts = msg.split(" ")
        msg = parts[0].strip()
        uname = getUserDisplayName(even['uid'])
        if even['uid'] in badfriends:
            responseToUser(even['uid'],u'抱歉 系統分析後認定你是壞朋友 小姍不會跟你學資訊 ')
            responseToUser(bossid, uname + u'試圖教以下事情然而小姍不接受 \n'+msg, botid)
            return "not learn"
        for bw in badwords:
            if bw in fullmsg:
                responseToUser(even['uid'],u'抱歉 系統分析後認定你是壞朋友 小姍不會跟你學:~ ')
                responseToUser(bossid, uname + u'試圖教以下事情然而小姍不接受 \n'+msg, botid)
                return "not learnn"
        
        if len(msg) <= 2:
            responseToUser(even['uid'],u'抱歉 學習目標不能少於兩個字，你想要教我"'+msg+ u'" 但是單靠兩個字就希望人工智慧有絕對正確反映也太強人所難')
            responseToUser(bossid, uname + u'試圖教以下事情不過失敗了 \n'+msg, botid)
            return "not leart"
        
        res = " ".join(parts[1:]) 
        toInsert={u'pkey':msg, u'res':[res], u'similar':msg,u'uid':even['uid']}

        if botid != '':
            toInsert={u'q':msg, u'a':[res]}

        print(toInsert)
        r = es.index(index=indexname, doc_type='fb',  body=toInsert)
        es.indices.refresh(index=indexname)
        responseToUser(even['uid'],u'學到了~謝謝~')
        uname = getUserDisplayName(even['uid'])
        responseToUser(bossid, uname + u' 教會機器人以下事情 \n'+msg+" "+res, botid)
        return "ok"
    except:
        print(even)
        return "something wrong"
   

if __name__ == '__main__':
    import sys

    msg = sys.argv[1]

    # To try from command line
    tmp = {u'msg':msg,u'uid':'Uc9b95e58acb9ab8d2948f8ac1ee48fad'}
    #tmp = {u'msg':msg,u'uid':'Uc9b95e58acb9ab8d2948f8ac1ee48fad',u'botid':botid}

    print(lambda_handler(tmp, None))
    
