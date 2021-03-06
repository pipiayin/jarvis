#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import requests
import boto3
import sys
import json
import decimal
import random
import argparse
import time
import datetime
import decimal
 
def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj)
    raise TypeError

from nocheckin import XLineToken



dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table_log = dynamodb.Table('linelog')


def listGroup(days=0, botid = '' ):
    now = datetime.datetime.now().timestamp()
    allgid = []

    toCheck = 0
    if days != 0: 
        toCheck = now - (days*24*60*60)

    last = None
    while True :
        if last == None:
            r = table_log.scan()
        else :
            r = table_log.scan(ExclusiveStartKey=last)

        for item in r['Items']:
            toPrint = {}
            last = item
            toPrint['ts'] = int(item['ts'])
            if int(item['ts']) < int(toCheck):
                continue
            if botid != '' and 'botid' not in item:
                continue
            if botid != '' and item['botid'] != botid:
                continue

            if 'isGroup' in item and  item['isGroup'] == 'True':
                if item['uid'] not in allgid:
                    allgid.append(item['uid'])
                print(item)
 
        time.sleep(9)
        if 'LastEvaluatedKey' not in r or r['LastEvaluatedKey'] == None:
            break
        else:
            last = r['LastEvaluatedKey']

    for g in allgid:
        print(g)

def listLog(botid ='',uid=''):
    last = None
    while True :
        if last == None:
            r = table_log.scan()
        else :
            r = table_log.scan(ExclusiveStartKey=last)

        for item in r['Items']:
            if uid != '' and item['uid'] != uid:
                continue
            if botid != '' and 'botid' not in item:
                continue
            if botid != '' and item['botid'] != botid:
                continue


            if 'isGroup' in item  and item['isGroup'] == 'False' and 'resp' in item:

                s=json.dumps(item, default=decimal_default,ensure_ascii=False)
                print(s)
                #print(str(toPrint['ts'])+";; "+toPrint['uid']+";; "+toPrint['botid']+";; "+toPrint['msg']+ ";; "+toPrint['resp'])

        time.sleep(10)
 
        if 'LastEvaluatedKey' not in r or r['LastEvaluatedKey'] == None:
            break
        else:
            last = r['LastEvaluatedKey']


if __name__ == '__main__':
    bossid='Uc9b95e58acb9ab8d2948f8ac1ee48fad'
    parser = argparse.ArgumentParser(description='line user tool')
    parser.add_argument('--list','-l', action='store_true', help='list log')
    parser.add_argument('--listgroup','-g', action='store_true', help='list group')
    parser.add_argument('--uid','-u',default='', help='list only for this uid')
    parser.add_argument('--botid','-b',default='', help='list only for this bot')
    parser.add_argument('--lastdays','-d',default=0, help='list only past N days')

    args = parser.parse_args()
    if args.list :
        print("show all current log")
        listLog(uid = args.uid, botid = args.botid)
        exit(0)
    if args.listgroup :
        print("show all current group")
        listGroup(days= int(args.lastdays), botid = args.botid)
        exit(0)

