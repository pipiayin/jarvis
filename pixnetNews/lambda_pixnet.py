# -*- coding: utf-8 -*-

from __future__ import print_function 
import json
import boto3
import sys
import datetime
import random
from pixnetTool import getFansNews, getFoodNews
from twlocation import TWLOCATION

lambda_client = boto3.client('lambda')

def lambda_foodhandler(even, context):
    try:
        print("-----In Lambda_foodhandler---")
        # even format: {"uid": "botid": , "msg":"msg"}
        # TODO: at this moment, all callback assume go for lineResponse
        uid = '' 
        if 'uid' in even :
            uid = even['uid']
        else:
            return 

        oriMsg = even['msg']
        location = ''
        for l in TWLOCATION:
            if l in oriMsg:
                location = l
                break 
        
        print('location:'+ location)
        (resMsg, geo) = getFoodNews(location=location)
        if len(geo) > 0:
            print(geo)
            geo['title'] = '推薦美食地點'
            geo['type'] = 'location'
            toLineResponse={'uid':uid, 'msg':resMsg, 'geo':geo}
        else:
            toLineResponse={'uid':uid, 'msg':resMsg}
          

        lresponse = lambda_client.invoke(
             FunctionName='lineResponse',
             InvocationType='Event',
             LogType='None',
             ClientContext='string',
             Payload=json.dumps(toLineResponse),
         )

        return 
    except:
        print(even)
        print(sys.exc_info()[0])
        return "something wrong"
   

def lambda_fanshandler(even, context):
    try:
        print("-----In Lambda_lottery---")
        # even format: {"uid": "botid": , "callback":"lineResponse"}
        # TODO: at this moment, all callback assume go for lineResponse
        uid = '' 
        if 'uid' in even :
            uid = even['uid']
        else:
            return 

        print(even)
        msg = getFansNews()
        toLineResponse={'uid':uid, 'msg':msg}

        lresponse = lambda_client.invoke(
             FunctionName='lineResponse',
             InvocationType='Event',
             LogType='None',
             ClientContext='string',
             Payload=json.dumps(toLineResponse),
         )

        return 
    except:
        print(even)
        print(sys.exc_info()[0])
        return "something wrong"
   

if __name__ == '__main__':
    print("TODO: simple test script")
    import sys
    even = {u'uid': 'Uc9b95e58acb9ab8d2948f8ac1ee48fad' , u'msg':sys.argv[1]}

    lambda_foodhandler(even, None)

