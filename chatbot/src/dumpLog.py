#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import json
import requests
import boto3
import sys
import json
import decimal
from decimal import Decimal
import random
import argparse
import time
from nocheckin import XLineToken



dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table_log = dynamodb.Table('linelog')



def listLog(botid ='',uid=''):
    allUid = []
    i = 1
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
            toPrint['uid'] = item['uid']
            if uid != '' and toPrint['uid'] != uid:
                continue
            if botid != '' and 'botid' not in item:
                continue
            if botid != '' and item['botid'] != botid:
                continue

            if 'botid' in item:
                toPrint['botid'] = item['botid']
            else:
                toPrint['botid'] = ""
            if type(item['msg']) == type(''):
                toPrint['msg'] = item['msg']
            else:
                toPrint['msg'] = ''
            if 'resp' in item:
                toPrint['resp'] = item['resp']
            else:
                toPrint['resp'] = ''

            print(str(toPrint['ts'])+";; "+toPrint['uid']+";; "+toPrint['botid']+";; "+toPrint['msg']+ ";; "+toPrint['resp'])
 
        if 'LastEvaluatedKey' not in r or r['LastEvaluatedKey'] == None:
            break
        else:
            last = r['LastEvaluatedKey']


if __name__ == '__main__':
    bossid='Uc9b95e58acb9ab8d2948f8ac1ee48fad'
    parser = argparse.ArgumentParser(description='line user tool')
    parser.add_argument('--list','-l', action='store_true', help='list log')
    parser.add_argument('--uid','-u',default='', help='list only for this uid')
    parser.add_argument('--botid','-b',default='', help='list only for this bot')

    args = parser.parse_args()
    if args.list :
        print("show all current log")
        listLog(uid = args.uid, botid = args.botid)
        exit(0)

