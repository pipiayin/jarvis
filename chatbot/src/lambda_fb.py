#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# For handle Facebook message request

from __future__ import print_function 
from socialBrain import SocialBrain
import json
import requests
import boto3
import sys
import json
import time
import random


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
lambda_client = boto3.client('lambda')



def lambda_handler(even, context):
    try:
        print("-----get message ---")
        print(len(even['entry']))
        print(even)
        msg = even['entry'][0][u'messaging'][0]['message']['text']
        mid = even['entry'][0][u'messaging'][0]['message']['mid']
        uid = even['entry'][0][u'messaging'][0]['sender']['id']
        rid = even['entry'][0][u'messaging'][0]['recipient']['id']
        toLog = {'mid':mid, 'uid':uid, 'msg':msg, 'res':'','ts':0}
        res = {
            "recipient_id": rid,
            "message_id": mid
        }
        resp =""
        if mid != '' and uid != '' :
            print("invoke fbresponse lambda event")
            lresponse = lambda_client.invoke(
                FunctionName='fbresponse',
                InvocationType='Event',
                LogType='None',
                ClientContext='string',
                Payload=json.dumps(toLog),
            )

            toLog['res'] = resp
            toLog['ts'] = int(time.time())
            print("response (tolog->)"+str(toLog))
        else:
            print("no need to response")
 
        return 
    except:
        print(even)
        print(sys.exc_info()[0])
        return "something wrong"
   

if __name__ == '__main__':
    import sys

    msg = sys.argv[1]

    # To try from command line
    print("TO DO...testing here")
