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

learn_trigger = '590590 '

def lambda_handler(even, context):
   # try:
        print("-----get message ---")
        ts =  int(time.time())
        print(even) #

        uid = even['events'][0]['source']['userId']
        msg = even['events'][0]['message']['text']
    
        msg = msg.strip()
        toLog = {'uid':uid, 'ts':ts, 'line':even, 'msg':msg}
        if msg.startswith(learn_trigger) :
            print("to learn...")
            table_log.put_item(Item=toLog)
            lresponse = lambda_client.invoke(
                FunctionName='ailearn',
                InvocationType='Event',
                LogType='None',
                ClientContext='string',
                Payload=json.dumps(toLog),
            )
        else:
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
    tmp = {u'events':
          [{
            u'source': {'userId': u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'},
            u'message': {'text':msg}
           }]}

    print(lambda_handler(tmp, None))

    
