#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import boto3
import sys
import csv
from time import sleep

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table_msglog = dynamodb.Table('msglog')
#response = table.put_item(
#    Item={'pkey':u'測試一下', u'res':[u'想測試一下而已嗎',u'只是測試而已？'] })
#print(response)
testu='1456446681048768'

if __name__ == '__main__':
    allitem = table_msglog.scan()

    allusers = []
for i in allitem['Items']:
    print(i)
    sleep(1)
           
  

