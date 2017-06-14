# -*- coding: utf-8 -*-

from __future__ import print_function 
import json
import boto3
import sys
import datetime
import random

from boto3.dynamodb.conditions import Key
from weatherFeed import getNotify

lambda_client = boto3.client('lambda')

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table_event = dynamodb.Table('lineevent')

def getRegisterUsers(eventName='weathernotify'):
    result = []
    response = table_event.query(
        IndexName='eventName-index',
        KeyConditionExpression=Key('eventName').eq(eventName)
    )
    for u in response['Items']:
        result.append(u['uid'])
    
    return result
    
def lambda_handler(even, context):
    """
    This lambda should be trigger by schedule
    """
    try:
        print("-----In Lambda_weathernotify---")
        weatherNotify = getNotify(1) # Get past 1 hours
        for msg in weatherNotify:

            msg = msg + "\n http://www.cwb.gov.tw/"  
            toNotifyUsers = getRegisterUsers()
            for uid in toNotifyUsers:
                toLineResponse={'uid':uid, 'msg':msg}
                print(toLineResponse)

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
    lambda_handler({}, {})
    #print(getRegisterUsers())
