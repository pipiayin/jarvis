#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import json
import requests
import sys

if __name__ == '__main__':

    msg = sys.argv[1]
    s = open('apikey.so')
    apiKey =  s.readline().strip()
    s.close()
    headers = {'Content-Type': 'application/json', 'x-api-key':apiKey}

    #url = 'https://csul2m26h5.execute-api.us-east-1.amazonaws.com/prod/ai'
    url = 'https://ns67c2h3na.execute-api.us-east-1.amazonaws.com/prod/ai'
    tmp =   {u'entry': [{u'messaging': [{u'timestamp': 1472454587950, u'message': {u'text': msg, u'mid': u'mid.1482454587943:6009b68089c825cf43', u'seq': 668}, u'recipient': {u'id': u'1739093062995859'}, u'sender': {u'id': u'2181896645200579'}}] , u'id': u'1739093062995859', u'time': 1472454587999}], u'object': u'page'}
    payload = json.dumps(tmp)
    r = requests.post(url, headers=headers, data = payload)
    resj = json.loads(r.text)
    print(resj)
