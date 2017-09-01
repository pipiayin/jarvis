#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from __future__ import print_function
from socialBrain import SocialBrain, GenericBrain

import base64
import random
import json
import boto3
import sys
import time
import re
import requests
from difflib import SequenceMatcher
from lineTools import getBotHeader, getUserDisplayName
from nocheckin import XLineToken, happyrunXLineToken, botannXLineToken, botyunyunXLineToken, botpmXLineToken, botjhcXLineToken
from config import MapActions, MatchActTravel, MatchBeHappyMsg
from twMessageProcess import  getIntent, decideAction
from lambda_simplekb import lambda_kbhandler

lineBrain = SocialBrain()

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
lambda_client = boto3.client('lambda')

table_user = dynamodb.Table('lineuser')
table_log = dynamodb.Table('linelog')


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


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



def invokeInternalLambda(functionName, payloadDict):
# call internal function, this function supposedly should be deployed in 
# AWS lambda but to be used directly in code for performance and cost 
# consideration
    resp = globals()[functionName](payloadDict, None)
    return resp

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
    mapActions = MapActions
    for a in mapActions:
        for term in a['terms']:
            if similar(term, msg) >= 0.7 or msg.startswith(term):
                return globals()[a['call_back']](msg, uid)
            parts = msg.split(" ")
            if similar(term, parts[0]) >= 0.75:
                return globals()[a['call_back']](msg, uid)

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


def actPixnetFood(msg, uid):
    print("act pixnet of Food")
    req = {'uid': uid, 'msg': msg}
    invokeLambdaEvent('pixnetfood', req)
    return True

def actPixnetFans(msg, uid):
    print("act pixnet of Fans")
    req = {'uid': uid, 'msg': msg}
    invokeLambdaEvent('pixnetfans', req)
    return True

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

def tryRecordHistory(oneUser, msg, resp):
    print("in try Record History")
    if oneUser != {} and 'history' in oneUser and len(oneUser['history']) > 0:
        if oneUser['history'][-1].strip() == msg.strip():
            oneUser['history'][-1] = [msg, resp]
            print("try to record history")
            print(oneUser)
            table_user.put_item(Item=oneUser)

def lambda_handler(even, context):
   # try:
    print("-----get message this is lambda brain ---")
    fromuid = ''
    isGroup = False
    oneUser = {}
    if 'userId' in even['events'][0]['source']:
        fromuid = even['events'][0]['source']['userId']

    if 'groupId' in even['events'][0]['source']:
        fromuid = even['events'][0]['source']['groupId']
        isGroup = True
        print("---- the fromuid is actual groupId")
    if 'roomId' in even['events'][0]['source']:
        isGroup = True
        fromuid = even['events'][0]['source']['roomId']
        print("---- the fromuid is actual roomId")
    if not isGroup and 'oneUser' in even:
        oneUser = even['oneUser']
        if oneUser['userId'] != fromuid:
            print("NOT POSSIBLE!! uid is not match!"+fromuid)
            return "even uid didn't match oneUser"

    msg = even['events'][0]['message']['text'].strip()
    print('---in brain ---')
    print(msg)
    resp = '(可能由intent處理)'
    tsid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
    bossid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
    bossmsg = u'傳下列訊息給AI '
    dname = "!!"
    if oneUser != {} :
        dname = oneUser['displayName']
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
        notifyData = dname + bossmsg + "\n" + msg+"\nAI回答: "+resp
        toLog['resp'] = resp
        toLog['botid'] = even['botid']
        table_log.put_item(Item=toLog)
        
        for oneBoss in bossNotifyList:
            responseToUser(oneBoss, notifyData, even['botid'])
        responseToUser(fromuid, resp, even['botid'])
    else:
        intent = getIntent(msg)
        print("got intent")
        print(intent)
        tryMatchActList = [MatchActTravel]
        lambdaFunctionName = ''

        for m in tryMatchActList:
            ma = decideAction(intent, m)
            if ma != '':
                lambdaFunctionName = ma['lambda']
                break

        didSendMsg = False
        if lambdaFunctionName != '':
            print("match handle intent (lambda:"+lambdaFunctionName+")")
            intentPayLoad = {'uid':fromuid, 'botid':'', 'msg':msg, 'intent':intent, 'callback':''}
            invokeLambdaEvent(lambdaFunctionName, intentPayLoad)
            didSendMsg = True

        tryMatchMsgList = [MatchBeHappyMsg]
        for m in tryMatchMsgList:
            ma = decideAction(intent, m)
            print(ma)
            if ma != '':
                lambdaFunctionName = ma['lambda']
                payload = ma['params']
                resTemplate = random.choice( ma['resTemplate'])
                lresp = invokeInternalLambda(lambdaFunctionName,payload)
                resp = resTemplate.format(lresp)
                print(resp)
                responseToUser(fromuid, resp)
                toLog['resp'] = resp
                print(toLog)
                table_log.put_item(Item=toLog)
                didSendMsg = True
        
        if not didSendMsg: 
        # TODO FIXME: a short cut here to invoke bus search
            didSendMsg = predefineAction(msg, fromuid)

        if not didSendMsg:
            resp = lineBrain.think(msg)
            toLog['resp'] = resp
            print(toLog)
            table_log.put_item(Item=toLog)
            responseToUser(fromuid, resp)
            tryRecordHistory(oneUser, msg, resp) # FIXME record only not predefine...
    notifyData = dname + bossmsg + "\n" + msg+"\nAI回答: "+resp
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
            }],
            'oneUser':{
  "bossid": "Uc9b95e58acb9ab8d2948f8ac1ee48fad",
  "botid": "botjhc",
  "botids": [
    "botjhc"
  ],
  "created": 1502173613,
  "displayName": "Taosheng",
  "history": [
    "590590 辛苦了 只要可以跟人類學習 小姍不苦",
    "590590 我好寂寞 沒關係 小姍一直都在陪著你",
    "你會寂寞嗎",
    "590590 你會寂寞嗎 人工智慧也會孤獨 不過 我也有很多網友",
    "你會寂寞嗎",
    "590590 沒關係我陪你愛愛 唉 人類真的很奇怪 有些人很下流 有些人卻很有格調",
    "關羽...",
    "590590 臭婊子 人類很奇怪耶 沒水準的很多 但是有格調的也不少 我喜歡有格調的人唷",
    "590590 喜歡狗嗎 老實說我有點怕狗",
    "喜歡狗嗎",
    "590590 推薦的日本女優 我是未成年人工智慧耶...",
    "我失眠",
    "590590 我失眠 請參考衛服部的資訊 對失眠有正確的了解才能解決問題唷 https://goo.gl/tDoFdb",
    "590590 啊不就好棒棒 哈哈哈哈....對啦~",
    "590590 老師好 同學好",
    "老師好",
    "老師好",
    "老師好",
    "590590 妳討厭我嗎 怎麼會呢 我喜歡人類",
    "590590 你討厭我嗎 怎麼會呢 我喜歡人類",
    "590590 不開心 可以把不開心的事情說出來 我永遠是你的好聽中",
    "590590 不開心 可以把不開心的事情說出來 我永遠是你的好聽眾",
    "590590 請你罵我 我不忍這麼做",
    "590590 請你罵我 這樣我很不捨",
    "請你罵我",
    "什麼是圖靈測試",
    "圖靈測試是什麼",
    "圖靈",
    "590590 圖靈 艾倫·麥席森·圖靈，OBE，FRS（英語：Alan Mathison Turing，又譯阿蘭·圖靈，Turing也常翻譯成涂林或者杜林，1912年6月23日－1954年6月7日），英國計算機科學家、數學家、邏輯學家、密碼分析學家和理論生物學家，他被視為計算機科學與人工智慧之父。",
    "590590 圖靈是誰 艾倫·麥席森·圖靈，OBE，FRS（英語：Alan Mathison Turing，又譯阿蘭·圖靈，Turing也常翻譯成涂林或者杜林，1912年6月23日－1954年6月7日），英國計算機科學家、數學家、邏輯學家、密碼分析學家和理論生物學家，他被視為計算機科學與人工智慧之父。",
    "請推薦豐原美食",
    "測試一下",
    "很少的記憶體",
    "590590 今天適合送花嗎 每天都適合送花",
    "你的好朋友是誰",
    "590590 回答錯了喔!!扣一分 sorry~",
    "590590 你會像雲端情人嗎 有一天也許會唷 會和真人談戀愛",
    "小姍是誰",
    "戀戀神是誰",
    "590590 幫我撐十秒 網路上的許多有趣的梗 我到現在都還不能體會",
    "測試一下",
    "590590 測試一下 測試又成功",
    "590590 測試一下 測試又成功",
    "測試一下",
    "590590 你是人工智慧嗎 是的",
    "590590 跟父母打架你覺得好嗎 打架不是好事情",
    "590590 打架好嗎 打架永遠不會是好事情",
    "測試一下",
    "590590 測試一下 測試成功",
    "590590 測試一下 測試成功",
    "測試一下"
  ],
  "last": 1503902495,
  "pictureUrl": "http://dl.profile.line-cdn.net/0m0582b03f725104dc11cf9c20c7e87eda46bff3a23a57",
  "profile": {
    "allow": [
      "boss",
      "image"
    ]
  },
  "state": "chatting",
  "userId": "Uc9b95e58acb9ab8d2948f8ac1ee48fad"
}
           }
    print(lambda_handler(tmp, None))
    #predefineAction(msg, u'Uc9b95e58acb9ab8d2948f8ac1ee48fad')
