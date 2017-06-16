from __future__ import print_function
import json
import boto3
import sys
import datetime
import random

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table_event = dynamodb.Table('lineevent')


def registEvent(eventName, uid):
    eventId = eventName+"_"+uid
    existReg = table_event.get_item( Key={ 'eventId': eventId })
    if "Item" in existReg:
        existReg['Item']['status'] = 'active' 
        table_event.put_item(Item=existReg['Item']) # just make sure 'active'
    else:
        newReg = {}
        newReg['eventId'] = eventId
        newReg['uid'] = uid
        newReg['eventName'] = eventName
        newReg['status'] = 'active'
        table_event.put_item(Item=newReg)
 
    
def unRegistEvent(eventName, uid):
    eventId = eventName+"_"+uid
    existReg = table_event.get_item( Key={ 'eventId': eventId })
    if "Item" in existReg:
        existReg['Item']['status'] = 'inactive' 
        table_event.put_item(Item=existReg['Item']) # just make sure 'active'

if __name__ == '__main__':
    registEvent('weathernotify','Ub6eef5ae850ac685c548a90e66c06201')
    registEvent('weathernotify','Uc9b95e58acb9ab8d2948f8ac1ee48fad')
    unRegistEvent('weathernotify','Uc9b95e58acb9ab8d2948f8ac1ee48fad')
    registEvent('weathernotify','Uc9b95e58acb9ab8d2948f8ac1ee48fad')
    registEvent('myth','Uc9b95e58acb9ab8d2948f8ac1ee48fad')

