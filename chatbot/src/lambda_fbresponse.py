#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# For handle Facebook message request

from __future__ import print_function 
from socialEnBrain import GenericEnBrain

import json
import requests
import boto3
import sys
import json
import time
import random


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

#table_log = dynamodb.Table('msglog')

#tmp = {u'entry': [{u'messaging': [{u'timestamp': 1472454587950, u'message': {u'text': u'\u54ea\u908a\u53ef\u4ee5\u6293\u5230\u76ae\u5361\u4e18', u'mid': u'mid.1472454587942:6009b68089c825cf40', u'seq': 268}, u'recipient': {u'id': u'1739093062995859'}, u'sender': {u'id': u'1181896645200579'}}] , u'id': u'1739093062995859', u'time': 1472454587999}], u'object': u'page'}

#FBTOKEN='EAASfqRZCfuj4BABqBW0AuPVnGIVYJC9MudDTixyAxX0oZBicI8MN4qGYP3j29QwvvUotId0172KfXfaRvwt97OpsjTdpVN4OudoZBADQ6FbeeoT7d3gMbICEhDlEiWeVuJuS3utPKH1XfINrOI0emQyG6GZAuIryM5HYrYrm8QZDZD'
FBTOKEN='EAASfqRZCfuj4BANDikXxwR80RbLTKtmd0xwMf1Blh0wQ9FTyCGjD7UcwFqMHu4eGp1OAJMvVftkY9nuSDZCUm0fZCfLqWSEP3eNr1eIlGFFSTwHUvuygs3F3frOSBccDIpLeYDqy3ZAY0ETj3HACjtKYMWFwFWOjY0ACEZBK3MgZDZD'
FBURL = 'https://graph.facebook.com/v2.6/me/messages'

fbBrain = GenericEnBrain()

def responseToUser(uid,mid, resp):
    try:
        print("start to response")
        headers = {"Content-type": "application/json"}
        payload = {}
        payload['recipient'] = {"id":uid}
        payload['message'] = {"text":resp}
        payload['access_token'] = FBTOKEN
    
        jdump = json.dumps(payload)
        print(jdump)
        url = FBURL + "?access_token="+FBTOKEN
        r = requests.post(url, headers=headers, data = jdump)
        print(r)
        print(r.text)
        print("did send response")
        return ''
    except:
        return ''
        


def lambda_handler(even, context):
    try:
        print("-----get message ---")
        print(even)
        msg = even['msg']
        mid = even['mid']
        uid = even['uid']
        rid = even['rid']
        resp = ''
        resp = fbBrain.think(msg)
        responseToUser(uid,mid, resp)
 
        return resp
    except:
        print(even)
        print(sys.exc_info()[0])
        return "something wrong"
   

if __name__ == '__main__':
    import sys

    msg = sys.argv[1]

    # To try from command line
    # TODO
    print("TODO..")
