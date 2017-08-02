#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from __future__ import print_function 
import json
import time
import requests
from lineTools import getBotHeader, getUserDisplayName
from nocheckin import aws_access_key_id,aws_secret_access_key,XLineToken, happyrunXLineToken, botannXLineToken, botyunyunXLineToken, botpmXLineToken, botjhcXLineToken




def responseToUser(uid, resp, botid='',imageurl='',geo=None):
#    try:
        print("to response to line user, with botid:"+botid+"-end-")
        headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}


        if botid != '':
            botHeaders = getBotHeader(botid)
            if botHeaders != '':
                headers = botHeaders

        payload = { 
            "to": uid ,
            "messages":[{
                "type":"text",
                "text": resp
             },
             #{u'type': u'sticker',  u'packageId': u'3524', u'stickerId': u'2713770'}
             ]
        }  

        if imageurl != '':
            payload['messages'].append({'type':'image', "originalContentUrl":  imageurl, "previewImageUrl": imageurl})

        if geo is not None and type(geo) == type({}):
            payload['messages'].append(geo)

        jdump = json.dumps(payload)
        print(jdump)
        url = 'https://api.line.me/v2/bot/message/push'
        #url = 'https://trialbot-api.line.me/v1/events'
        print("----headers---")
        print(headers)
        r = requests.post(url, headers=headers, data = jdump)
        print(r.text)
        print("did send response")

        return ''
#    except:
#        return ''
        


def lambda_handler(even, context):
   # try:
        print("-----just response message to a uid ---")
        # all we need in even{} is uid, msg, botid
        botid = ''
        imageurl = ''
        if 'uid' in even and 'msg' in even:
            if 'botid' in even: 
                botid = even['botid']
            if 'imageurl'  in even:
                imageurl = even['imageurl']
        else:
            return
        geo = None
        if 'geo' in even:
            geo = even['geo']

        responseToUser(even['uid'],even['msg'],botid,imageurl,geo=geo)

        tsid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
        bossid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
        bossmsg = u'聊天機器人回傳訊息使用者 '
        dname = getUserDisplayName(even['uid'])
        ts =  int(time.time())
        if 'botid' in even :
            notifyData = dname + bossmsg +"\n"+ even['msg']
            for oneBoss in bossNotifyList:
                responseToUser(oneBoss,notifyData,even['botid'])
            #responseToToken(replyToken,resp,even['botid'])
        return
   # except:
   #     print(even)
   #     print(sys.exc_info()[0])
   #     return "something wrong"
   

if __name__ == '__main__':

    # To try from command line
    tmp={
        'uid':u'Uc9b95e58acb9ab8d2948f8ac1ee48fad',
         'msg':'a short url',}
         #'imageurl':'https://s3-us-west-2.amazonaws.com/sandyiface/Uc9b95e58acb9ab8d2948f8ac1ee48fad_6435271838359.jpg'}
    print(lambda_handler(tmp, None))

    
