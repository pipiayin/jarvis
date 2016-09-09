#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import json
import requests
import boto3
import sys
import json
import random


dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table_log = dynamodb.Table('linelog')


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

def showUids():
        allUid = []
        r = table_log.scan(Limit=5000)
        for item in r['Items']:
            oneUid = item['uid']
            if oneUid not in allUid:
                allUid.append(oneUid)
        for u in allUid:
            print(u)
        print(len(allUid))



if __name__ == '__main__':
    print(dir(table_log))
    showUids()

    # To try from command line
    
