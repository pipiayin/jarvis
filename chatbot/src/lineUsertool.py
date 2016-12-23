#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import json
import requests
import boto3
import sys
import json
import random
import argparse


dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table_log = dynamodb.Table('lineuser')
table_usert = dynamodb.Table('lineusert')
table_user = dynamodb.Table('lineuser')


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

def listLineUserId():
    allUid = []
    r = table_user.scan(Limit=5000)
    for item in r['Items']:
        allUid.append(item[u'userId'])
    return allUid
    

def showLineUsers():
        allUid = []
        r = table_user.scan(Limit=5000)
        cnt = 1
        for item in r['Items']:
            print(cnt)
            print(item)
            cnt += 1

def getUserSession(uid):
    item = table_user.get_item( Key={ 'userId': uid })

    if "Item" in item:
        return item['Item']
    else: 
        return None
def updateUserSession(uitem):
    table_user.put_item( Item = uitem)


if __name__ == '__main__':
    bossid='Uc9b95e58acb9ab8d2948f8ac1ee48fad'
    parser = argparse.ArgumentParser(description='line user tool')
    parser.add_argument('--list','-l', action='store_true', help='list all user')
    parser.add_argument('--msg','-m', help='send message to all user')

    args = parser.parse_args()
    if args.list :
        print("show all current line users")
        showLineUsers()
        exit(0)

    if args.msg is not None:
   
        print("send message:"+args.msg)
        ulist =  [bossid]
#        ulist = listLineUserId()
#        for iu in ulist:
#            print(iu)
    #showAll()
    #s = getUserSession(bossid)
    #s['lmsg'] = 'the last few words'
    #s['status'] = 'expecting'
    #print(s)
    #updateUserSession(s)

    # To try from command line
    

