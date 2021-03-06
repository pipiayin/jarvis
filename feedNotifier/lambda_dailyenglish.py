# -*- coding: utf-8 -*-

from __future__ import print_function 
import json
import boto3
import sys
import datetime
import random

from boto3.dynamodb.conditions import Key
from dailyEnglishFeed import getNotify

lambda_client = boto3.client('lambda')

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table_event = dynamodb.Table('lineevent')

def getRegisterUsers(eventName='dailyenglish'):
    result = []
    response = table_event.query(
        IndexName='eventName-index',
        KeyConditionExpression=Key('eventName').eq(eventName)
    )
    for u in response['Items']:
        if 'status' in u and u['status'] == 'active':
            result.append(u['uid'])
    
    return result
    
def lambda_handler(even, context):
    """
    This lambda should be trigger by schedule
    """
    try:
        print("-----In Lambda_dailyenglish---")
        weatherNotify = getNotify(24) # Get past 24 hours
        toNotifyUsers = getRegisterUsers()
        for msg in weatherNotify:
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
