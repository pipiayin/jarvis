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



def listLog():
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
            if 'botid' in item:
                toPrint['botid'] = item['botid']
            if type(item['msg']) == type(''):
                toPrint['msg'] = item['msg']
            if 'resp' in item:
                toPrint['resp'] = item['resp']

            print(json.dumps(toPrint))
 
        if 'LastEvaluatedKey' not in r or r['LastEvaluatedKey'] == None:
            break
        else:
            last = r['LastEvaluatedKey']


if __name__ == '__main__':
    bossid='Uc9b95e58acb9ab8d2948f8ac1ee48fad'
    parser = argparse.ArgumentParser(description='line user tool')
    parser.add_argument('--list','-l', action='store_true', help='list log')

    args = parser.parse_args()
    if args.list :
        print("show all current log")
        listLog()
        exit(0)

