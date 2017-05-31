# -*- coding: utf-8 -*-

from __future__ import print_function 
import json
import boto3
import sys
import datetime
import random
from dayFortuneTool import tellTheDay

lambda_client = boto3.client('lambda')

def lambda_handler(even, context):
#    try:
        print("-----In Lambda_dayfurtune---")
        # even format: {"uid": "botid": , "astro":"金牛, 雙子..etc"}
        # TODO: at this moment, all callback assume go for lineResponse
        uid = '' 
        if 'uid' in even :
            uid = even['uid']
        else:
            return 

        msg = tellTheDay(even['day']) # in string
        toLineResponse={'uid':uid, 'msg':msg}

        lresponse = lambda_client.invoke(
             FunctionName='lineResponse',
             InvocationType='Event',
             LogType='None',
             ClientContext='string',
             Payload=json.dumps(toLineResponse),
         )


        return 
#    except:
#        print(even)
#        print(sys.exc_info()[0])
#        return "something wrong"
   

if __name__ == '__main__':

    msg ={'uid':'Uc9b95e58acb9ab8d2948f8ac1ee48fad','day':u'19791212'}
    lambda_handler(msg,None)
