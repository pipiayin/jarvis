#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import json
import requests
import boto3
import sys
import json
import random
import argparse
import time
from nocheckin import XLineToken



dynamodb = boto3.resource('dynamodb', region_name='us-west-2')



table_log = dynamodb.Table('linelog')



def listLog():
    allUid = []
    r = table_log.scan(Limit=500000)
    for item in r['Items']:
        print(item)
    


if __name__ == '__main__':
    bossid='Uc9b95e58acb9ab8d2948f8ac1ee48fad'
    parser = argparse.ArgumentParser(description='line user tool')
    parser.add_argument('--list','-l', action='store_true', help='list log')

    args = parser.parse_args()
    if args.list :
        print("show all current log")
        listLog()
        exit(0)

