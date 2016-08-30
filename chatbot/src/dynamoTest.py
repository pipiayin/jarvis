#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import json
import requests
import boto3
import sys
import json
import random


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table_log = dynamodb.Table('msglog')


def exists(mid,uid):
    item = None
    try:
        item = table_log.get_item( Key={ 'mid': mid, 'uid':uid })
        if "Item" in item:
            return item
        else: 
            return None
    except:
        print(sys.exc_info()[0])
        item = None
    return item

if __name__ == '__main__':

    msg = sys.argv[1]

    # To try from command line
    tmp = {u'entry': [{u'messaging': [{u'timestamp': 1472454587950, u'message': {u'text': msg, u'mid': u'mid.1472454587942:6009b68089c825cf40', u'seq': 268}, u'recipient': {u'id': u'1739093062995859'}, u'sender': {u'id': u'1181896645200579'}}] , u'id': u'1739093062995859', u'time': 1472454587999}], u'object': u'page'}
    mid = 'mid.1472454587942:6009b68089c825cf40--'
    uid = '1181896645200579'
    print(exists(mid,uid))

    
