#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import requests
import boto3
import sys
import json
import random
import argparse
import time
import datetime
from nocheckin import XLineToken


dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table_log = dynamodb.Table('lineuser')
table_usert = dynamodb.Table('lineusert')
table_user = dynamodb.Table('lineuser')

def updateUserProfile(uid, profileString):
    profileList = profileString.split(".")
    item = table_user.get_item( Key={ 'userId': uid })
    if "Item" in item:
        oneUser = item['Item']
        if 'profile' in oneUser:
            if profileList[0] in oneUser['profile']:
                oneUser['profile'][profileList[0]].append(profileList[1])
            else:
                oneUser['profile'][profileList[0]] = [profileList[1]]
        else:
            oneUser['profile'] = {} 
            oneUser['profile'][profileList[0]] = [profileList[1]]
        table_user.put_item( Item = oneUser)
        print("done update")

     
def updateUserState(uid, state):
    item = table_user.get_item( Key={ 'userId': uid })
    if "Item" in item:
        oneUser = item['Item']
        oneUser['state'] = state
        table_user.put_item( Item = oneUser)
         

def getLineUser(uid):
        item = table_user.get_item( Key={ 'userId': uid })
        oneUser = {}
        n = datetime.datetime.now().timestamp()
        if "Item" in item:
#            return item['Item']
            oneUser = item['Item']
    
        if len(oneUser) > 0:
            return oneUser

        line_url = 'https://api.line.me/v2/bot/profile/' + uid
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}

        r = requests.get(line_url, headers=headers)
        rjson = json.loads(r.text)

        return rjson

def sendToUser(uid, msg):
#    try:
        print("send text to line user")
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}
        payload = {
            "to": uid ,
            "messages":[{
                "type":"text",
                "text": msg
             }]
        }

        jdump = json.dumps(payload)
        print(jdump)
        url = 'https://api.line.me/v2/bot/message/push'
        #url = 'https://trialbot-api.line.me/v1/events'
        r = requests.post(url, headers=headers, data = jdump)
        if "Failed" in r.text:
            print(r.text+" --> "+uid)

        return ''

def sendImageToUser(uid, imageurl):
        print("send image to line user")
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}
        payload = {
            "to": uid ,
            "messages":[{
                "type":"image",
                "originalContentUrl":  imageurl,
                "previewImageUrl": imageurl
             }]
        }

        jdump = json.dumps(payload)
        print(jdump)
        url = 'https://api.line.me/v2/bot/message/push'
        #url = 'https://trialbot-api.line.me/v1/events'
        r = requests.post(url, headers=headers, data = jdump)
        print(r.text)

        return ''

def sendImageToUserList(ulist, imageurl):
    for u in ulist:
        sendImageToUser(u, imageurl)
        time.sleep(0.5)
        print("done: "+u)

def sendToUserList(ulist, msg):
    for u in ulist:
        sendToUser(u, msg)
        time.sleep(0.5)
        print("done: "+u)

def exists(mid,uid):
    item = None
    try:
        item = table_log.get_item( Key={ 'mid': mid, 'uid':uid })
        if "Item" in item:
            return item
        else: 
            return None
    except:
        print(sys.exc_info()[0])
        item = None
    return item

def listLineUserId():
    allUid = []
    r = table_user.scan(Limit=5000)
    for item in r['Items']:
        allUid.append(item[u'userId'])
    return allUid
    

def showLineUsers(lastdays=None, historiesOnly=False):
    allUid = []
    cnt = 1
    last = None
    while True :
        if last == None:
            r = table_user.scan()
        else :
            r = table_log.scan(ExclusiveStartKey=last)

        for item in r['Items']:
            pictureUrl = ''
            if 'pictureUrl' in item:
                pictureUrl=item['pictureUrl']
            historiesNo = ''
            histories = ''
            if 'history'  in item:
                historiesNo = str(len(item['history']))
                for h in item['history']:
                    histories = histories +"\n"+str(h)
            tmp = "{},{},{},{},".format(item['userId'],pictureUrl,item['displayName'],historiesNo)
 #     {'displayName': 'Y G', 'pictureUrl': 'http://dl.profile.line-cdn.net/0hOw6jMh39EFgLEz8kzRBvDzdWHjV8PRYQcyFbOS0VRmEuIlVaYiFcPyxEG28mIgILMn0PPSwWTG4i', 'userId': 'Ua60d254375033b0a8cd170dab02ea453', 'statusMessage': '思念太猖狂(煩惱)', 'last': Decimal('1497232992')}
            n = datetime.datetime.now().timestamp()

            if 'created' in item:
                cd = datetime.datetime.fromtimestamp(item['created'])
                tmp = tmp + cd.isoformat()
             
            tmp = tmp +","
            if lastdays is not None and 'last' in item:
                toCheck = n - (lastdays*24*60*60)
                last = item['last']
                tmp = tmp + str(last)
                if int(last) >= int(toCheck):
                    print(tmp)

            elif lastdays is None:
                tmp = tmp +","
                print(tmp)
            else:
                pass
            if historiesOnly:
                print(histories)
            cnt += 1

        time.sleep(1)
        if 'LastEvaluatedKey' not in r or r['LastEvaluatedKey'] == None:
            break
        else:
            last = r['LastEvaluatedKey']

def getUserSession(uid):
    item = table_user.get_item( Key={ 'userId': uid })

    if "Item" in item:
        return item['Item']
    else: 
        return None

def updateUserSession(uitem):
    table_user.put_item( Item = uitem)


if __name__ == '__main__':
    bossid='Uc9b95e58acb9ab8d2948f8ac1ee48fad'
    parser = argparse.ArgumentParser(description='line user tool')
    parser.add_argument('--list','-l', action='store_true', help='list all user')
    parser.add_argument('--msg','-m', help='send message to all user')
    parser.add_argument('--select','-s', help='selected user list file')
    parser.add_argument('--profile','-p', help='get one user profile')
    parser.add_argument('--updateState','-u', help='update one user state (with -p)')
    parser.add_argument('--updateProfile','-U', help='update one user profile (with -p)')
    parser.add_argument('--lastdays','-d', help='show only user who actually use in past N days')
    parser.add_argument('--imageurl','-i', help='message attached image url') 
    parser.add_argument('--historiesOnly','-H',action='store_true', help='list only conversation history (for analysis purpose)') 

    args = parser.parse_args()
    if args.updateProfile is not None:
        if args.profile is None:
            print("need to specify user id")
        else:
            print("to update " + args.profile + " "+ args.updateProfile)
            if args.updateProfile == 'allow.image':
     
                updateUserProfile(args.profile, args.updateProfile)
        exit(0)
    if args.profile is not None :
        if args.updateState is not None:
            print("update single user state to:" + args.updateState)
            updateUserState(args.profile, args.updateState)
        else:
            print("show single user profile")
        print(getLineUser(args.profile))
        exit(0)

    if args.list :
        print("show all current line users")
        lastdays = None
        if args.lastdays is not None:
            lastdays = float(args.lastdays)
        showLineUsers(lastdays, args.historiesOnly)
        exit(0)

    if args.msg is not None:
        print("send message:" + args.msg)
        if args.imageurl is not None:
            print("with image"+args.imageurl)
        ulist =  [bossid]
        if args.select is not None:
            userListFile = open(args.select)
            for line in userListFile:
                parts = line.split(",")
                uid=parts[0].strip()
                ulist.append(uid)
#            print(ulist)
            if args.imageurl is not None:
                sendImageToUserList(ulist,args.imageurl)

            sendToUserList(ulist,args.msg)
        else:
            ulist = listLineUserId()
            print(ulist)
            if args.imageurl is not None:
                sendImageToUserList(ulist,args.imageurl)
            sendToUserList(ulist,args.msg)

