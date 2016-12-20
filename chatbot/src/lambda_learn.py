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
from nocheckin import aws_access_key_id,aws_secret_access_key,XLineToken

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


learn_trigger = '590590 '
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


def responseToUser(uid, resp):
#    try:
        print("to response to line user")
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}
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
        if not msg.startswith(learn_trigger):
            print('should not learn things here !!')
            return ''
        msg = msg.replace(learn_trigger,'')
        parts = msg.split(" ")
        msg = parts[0]
        res = " ".join(parts[1:])
        toInsert={u'pkey':msg, u'res':[res], u'similar':msg}
        res = es.index(index="testi", doc_type='fb',  body=toInsert)
        es.indices.refresh(index="testi")
        responseToUser(even['uid'],u'學到了~謝謝~')
        uname = getUserDisplayName(even['uid'])
        responseToUser(bossid,uname+u' 教會小姍： \n'+msg+"::"+res)
        return "ok"
    except:
        print(even)
        return "something wrong"
   

if __name__ == '__main__':
    import sys

    msg = sys.argv[1]

    # To try from command line
    tmp = {u'msg':msg,u'uid':'Uc9b95e58acb9ab8d2948f8ac1ee48fad'}

    print(lambda_handler(tmp, None))

    
