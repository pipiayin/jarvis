#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import sys
import boto3
from boto3.dynamodb.conditions import Key, Attr
import csv
import json
import random
import time
import datetime
import argparse
from nocheckin import XLineToken

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table_log = dynamodb.Table('linelog')
table_group = dynamodb.Table('linegroup')

def toCheckTimestamp(days=0):
    n = datetime.datetime.now().timestamp()
    toCheck = 0
    if days > 0:
        toCheck = int(n - (days*24*60*60))
    return toCheck
    
def listAllGroup(days=0):
    toCheck = toCheckTimestamp(days)
    last = None
    uidList = []
    response = table_log.query(
        TableName='linelog',
        IndexName='isGroup-ts-index',
        KeyConditionExpression=Key('isGroup').eq('True') & Key('ts').gt(toCheck) 
    )

    while(True):

        for item in response['Items']:
            if item['uid'] not in uidList:
                uidList.append(item['uid'])

        if 'lastEvaluateKey' in response:
            last = response['lastEvaluateKey']
            response = table_log.query(
                TableName='linelog',
                IndexName='isGroup-ts-index',
                KeyConditionExpression=Key('isGroup').eq('True') & Key('ts').gt(toCheck) ,
                ExclusiveStartKey = last 
            )
        else:
            break

    print(len(uidList))
    for g in uidList:
        print(g)


def showGroupLog(days=0):
    toCheck = toCheckTimestamp(days)

    response = table_log.query(
        TableName='linelog',
        IndexName='isGroup-ts-index',
        KeyConditionExpression=Key('isGroup').eq('True') & Key('ts').gt(toCheck)    )

    uidList = []
    for item in response['Items']:
        print(item)
        if item['uid'] not in uidList:
            uidList.append(item['uid'])
   

if __name__ == '__main__':
    bossid='Uc9b95e58acb9ab8d2948f8ac1ee48fad'
    parser = argparse.ArgumentParser(description='line group tool')
    parser.add_argument('--list','-l', action='store_true', help='list all group')
    parser.add_argument('--showlog','-g',action='store_true',help='show log')
    parser.add_argument('--msg','-m', help='send message to all group')
    parser.add_argument('--select','-s', help='selected group list file')
    parser.add_argument('--groupid','-i', help='specify group id')
    parser.add_argument('--lastdays','-d', help='show only group who actually use in past N days', default=0)

    args = parser.parse_args()
    if args.list :
        ldays = 0 
        listAllGroup(days=int(args.lastdays))
        exit(0)

    if args.showlog:
        showGroupLog(days=int(args.lastdays))
        exit(0)

