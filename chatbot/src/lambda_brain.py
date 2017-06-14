#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from __future__ import print_function
from socialBrain import SocialBrain, GenericBrain

import json
import boto3
import sys
import time
import re
import requests
from difflib import SequenceMatcher

from nocheckin import XLineToken, happyrunXLineToken, botannXLineToken, botyunyunXLineToken, botpmXLineToken, botjhcXLineToken

lineBrain = SocialBrain()

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
lambda_client = boto3.client('lambda')

table_log = dynamodb.Table('linelog')


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def getBotHeader(botid):
    botMap = {'happyrun': happyrunXLineToken,
              'botann': botannXLineToken,
              'botpm': botpmXLineToken,
              'botjhc': botjhcXLineToken,
              'botyunyun': botyunyunXLineToken}
    if botid in botMap:
        headers = {"Content-type": "application/json; charset=utf-8",
                   "Authorization": "Bearer " + botMap[botid]}
        return headers
    else:
        return ""


def responseToToken(replyToken, resp, botid=''):
#    try:
    print("to response to line replytoken")
    headers = {"Content-type": "application/json; charset=utf-8",
               "Authorization": "Bearer " + XLineToken}

    if botid != '':
        botHeaders = getBotHeader(botid)
        if botHeaders != '':
            headers = botHeaders

    payload = {
        "replyToken": replyToken,
        "messages": [{
            "type": "text",
            "text": resp
        }]
    }

    jdump = json.dumps(payload)
    print(jdump)
    url = 'https://api.line.me/v2/bot/message/reply'
    # url = 'https://trialbot-api.line.me/v1/events'
    r = requests.post(url, headers=headers, data=jdump)
    print(r.text)
    print("did send response")
    return ''


def responseToUser(uid, resp, botid=''):
#    try:
    print("to response to line user, with botid:" + botid + "-end-")
    headers = {"Content-type": "application/json; charset=utf-8",
               "Authorization": "Bearer " + XLineToken}

    if botid != '':
        botHeaders = getBotHeader(botid)
        if botHeaders != '':
            headers = botHeaders

    payload = {
        "to": uid,
        "messages": [{
            "type": "text",
            "text": resp
        }]
    }

    jdump = json.dumps(payload)
    print(jdump)
    url = 'https://api.line.me/v2/bot/message/push'
    # url = 'https://trialbot-api.line.me/v1/events'
    print("----headers---")
    print(headers)
    r = requests.post(url, headers=headers, data=jdump)
    print(r.text)
    print("did send response")

    return ''
#    except:
#        return ''


def getUserDisplayName(fromuid, botid=''):
    try:
        line_url = 'https://api.line.me/v2/bot/profile/' + fromuid
        headers = {"Content-type": "application/json; charset=utf-8",
                   "Authorization": "Bearer " + XLineToken}

        if botid != '':
            botHeaders = getBotHeader(botid)
            if botHeaders != '':
                headers = botHeaders

        r = requests.get(line_url, headers=headers)
        rjson = json.loads(r.text)
        ruser = rjson['displayName']
        return ruser
    except:
        print('can not get displayName from uid:' + fromuid)
        return ''


def invokeLambdaEvent(functionName, payloadDict):
    lresponse = lambda_client.invoke(
        FunctionName=functionName,
        InvocationType='Event',
        LogType='None',
        ClientContext='string',
        Payload=json.dumps(payloadDict),
    )
    print(lresponse)


def predefineAction(msg, uid):
    msg = msg.strip()
    msg = msg.replace("「",'').replace("」",'')
    
    #TODO find a better mapping way instead of hardcoding
    mapActions = [
        { 'call_back': actEventReg,
          'terms' :
                    [u'請通知我天氣特報' ,
                     u'請通知激烈天氣特報',
                     u'小姍請通知我天氣特報',
                     u'小姍通知我激烈天氣特報',
                     u'通知激烈天氣特報',
                     u'請每天教我一句英文',
                     u'請給我每日一句學英文',
                     u'小姍請給我每日一句學英文',
                     u'小姍給我每日一句學英文',
                     u'每日一句學英文',
                     u'自動給我每日一句學英文',
                     u'通知天氣特報',]
        },
        {'call_back': actWishes,
         'terms': [u'我想許願']
         },
        {'call_back': actTaipeiBus,
         'terms': [u'幫我查公車', u'請幫我查公車', u'小姍幫我查公車', u'公車在哪裡', u'請幫我查公車']
         },
        {'call_back': actLottery,
         'terms': [u'幫我抽根籤', u'請幫我抽個籤', u'小姍幫我抽簽', u'幫我抽簽看看', u'再幫我抽一次', u'請幫我抽支籤', u'請幫大姐抽支籤', u'請幫我抽籤']
         },
        {'call_back': actAstro,
         'terms': [u'今天星座運勢', u'跟我說今天星座運勢', u'小姍幫我查星座運勢', u'幫我看星座運勢', u'幫我查今日星座運勢', u'今日星座運勢',u'小姍幫我查今日星座']
         },
        {'call_back': actDayfortune,
         'terms': [u'幫我算命 ', u'出生運勢', u'小姍幫我查出生運勢', u'幫我看出生運勢', u'請幫我算命 生日是', u'請幫我算命',u'幫我算命生日是',u'請幫我算命生日是']
         }
    ]
    for a in mapActions:
        for term in a['terms']:
            if similar(term, msg) >= 0.7 or msg.startswith(term):
                return a['call_back'](msg, uid)
            parts = msg.split(" ")
            if similar(term, parts[0]) >= 0.75:
                return a['call_back'](msg, uid)

    return False


def actWishes(msg, uid):
    responseToUser(uid, u'您的願望已經被記錄下來...希望有朝一日會實現')
    return True

def actDayfortune(msg, uid):
    match = re.search(r'([0-9]{8})', msg)
    if len(match.groups()) >= 1:
        bdate = match.group(1)
        dayReq = {'uid': uid, 'day': bdate}
        invokeLambdaEvent('dayfortune', dayReq)
        return True

    return False


def actAstro(msg, uid):
    print("act Astro")
    astroList = {"水瓶": ["水瓶", "寶瓶", "水平"], "雙魚": ["雙魚", '双魚'], "牡羊": ["牡羊", '白羊'], "金牛": ["金牛"], "雙子": ["雙子", "双子"], "巨蟹": [
        "巨蟹"], "獅子": ["獅子"], "處女": ["處女", "室女"], "天秤": ["天秤", "天枰", "天平"], "天蠍": ["天蠍"], "射手": ["射手", "人馬"], "魔羯": ["摩羯", "山羊"]}

    astro = ""
    for aName, nNames in astroList.items():
        for nName in nNames:
            if nName in msg:
                astro = aName
                astroReq = {'uid': uid, 'astro': astro}
                invokeLambdaEvent('astro', astroReq)
                return True

    return False


def actTaipeiBus(msg, uid):
    print("act TaipeiBus")
    busname = msg.strip().replace(u'幫我查公車', '').replace(" ", "")
    taipeiBusReq = {'uid': uid, 'busname': busname}
    invokeLambdaEvent('taipeibus', taipeiBusReq)
    return True


def actLottery(msg, uid):
    print("act Lottery")
    lotteryReq = {'uid': uid, 'botid': "", 'msg': msg}
    invokeLambdaEvent('lottery', lotteryReq)
    return True

def actEventReg(msg, uid):
    print("act register event")
    req = {'uid': uid, 'botid': "", 'evenName': msg}
    invokeLambdaEvent('eventreg', req)
    return True

def lambda_handler(even, context):
   # try:
    print("-----get message this is lambda brain ---")
    fromuid = ''
    if 'userId' in even['events'][0]['source']:
        fromuid = even['events'][0]['source']['userId']
    if 'groupId' in even['events'][0]['source']:
        fromuid = even['events'][0]['source']['groupId']
        print("---- the fromuid is actual groupId")
    if 'roomId' in even['events'][0]['source']:
        fromuid = even['events'][0]['source']['roomId']
        print("---- the fromuid is actual roomId")

    msg = even['events'][0]['message']['text']
    resp = ''
    tsid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
    bossid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
    bossmsg = u'傳下列訊息給聊天機器人 '
    dname = getUserDisplayName(fromuid)
    ts = int(time.time())
    toLog = {'uid': fromuid, 'ts': ts, 'line':
             even['events'], 'msg': msg, 'resp': ""}
    if 'botid' in even:
        genericBrain = GenericBrain(even['botid'], 'q')
        bossid = even['bossid']
        bossNotifyList = [bossid]
        if 'bossids' in even:
            bossNotifyList = bossNotifyList + even['bossids']
        bossmsg = bossmsg + even['botid'] + " "
        resp = genericBrain.think(msg)
        notifyData = dname + bossmsg + "\n" + msg
        toLog['resp'] = resp
        toLog['botid'] = even['botid']
        table_log.put_item(Item=toLog)
        for oneBoss in bossNotifyList:
            responseToUser(oneBoss, notifyData, even['botid'])
        responseToUser(fromuid, resp, even['botid'])
    else:
        # TODO FIXME: a short cut here to invoke bus search
        didSendMsg = predefineAction(msg, fromuid)

        if not didSendMsg:
            resp = lineBrain.think(msg)
            toLog['resp'] = resp
            print(toLog)
            table_log.put_item(Item=toLog)
            responseToUser(fromuid, resp)

    notifyData = dname + bossmsg + "\n" + msg
    responseToUser(tsid, notifyData)
    return "ok"
   # except:
   #     print(even)
   #     print(sys.exc_info()[0])
   #     return "something wrong"


if __name__ == '__main__':
    msg = sys.argv[1]

    # To try from command line
    tmp = {u'events':
           [{
            u'source': {'userId': u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'},
            u'message': {'text': msg}
            }]}
    print(lambda_handler(tmp, None))
    predefineAction(msg, u'Uc9b95e58acb9ab8d2948f8ac1ee48fad')
