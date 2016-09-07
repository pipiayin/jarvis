#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from __future__ import print_function 
import json
import boto3
import sys
import json
import time
import random
import botocore.session


dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table_log = dynamodb.Table('linelog')
lambda_client = boto3.client('lambda')



def lambda_handler(even, context):
   # try:
        print("-----get message ---")
        ts =  int(time.time())
        uid = even['result'][0]['content']['from']
        msg = even['result'][0]['content']['text']
        toLog = {'uid':uid, 'ts':ts, 'line':even, 'msg':msg}
        table_log.put_item(Item=toLog)
        lresponse = lambda_client.invoke(
            FunctionName='aibrain',
            InvocationType='Event',
            LogType='None',
            ClientContext='string',
            Payload=json.dumps(even),
        )
        print("responsed (tolog->)"+str(toLog))
        return "ok"
   # except:
        print(even)
        print(sys.exc_info()[0])
        return "something wrong"
   

if __name__ == '__main__':
    import sys

    msg = sys.argv[1]

    # To try from command line
    tmp = { "result":[ { "from":"u206d25c2ea6bd87c17655609a1c37cb8", "fromChannel":1341301815, "to":["u0cc15697597f61dd8b01cea8b027050e"], "toChannel":1441301333, "eventType":"138311609000106303", "id":"ABCDEF-12345678901", "content":{ } } ] }
    print(lambda_handler(tmp, None))

    