#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import boto3
import sys
import csv
from time import sleep
import json
import requests
import random
import time


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table_msglog = dynamodb.Table('msglog')
#response = table.put_item(
#    Item={'pkey':u'測試一下', u'res':[u'想測試一下而已嗎',u'只是測試而已？'] })
#print(response)
testu='1244918332196197'
testu='1285621614790666'

access_token = ''


def getResponse(path, params={}):
    params['access_token'] = access_token
    r = requests.get('https://graph.facebook.com/v2.6/'+path,params=params)
    #print(r)
    #print(r.text)
    return json.loads(r.text)

def grepUser(cuser,params={}):
    params['access_token'] = access_token
    user = getResponse('/'+cuser, params)
    return user


if __name__ == '__main__':

    s = open('secret.so')
    client_secret= s.readline().strip()
    s.close()


    app_id = '1301448639887934'

    r = requests.get('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id='+app_id+'&client_secret='+client_secret)
    access_token = r.text.split('=')[1]
    print("access-token")
    print(access_token)
    params_user={'fields':'id,about,bio,name,link'}
    
    print(grepUser(testu,params_user))
