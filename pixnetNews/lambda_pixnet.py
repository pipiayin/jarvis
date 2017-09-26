# -*- coding: utf-8 -*-

from __future__ import print_function 
import json
import boto3
import sys
import datetime
import random
from pixnetTool import getFansNews, getFoodNews, getTravelNews
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
        (resMsg, geo) = getFoodNews(location=location, kuso=True)
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
   

def lambda_travelhandler(even, context):
    #try:
        print("-----In Lambda_travelhandler---")
        # even format: {"uid": "botid": , "callback":"lineResponse","msg":"search msg","intent":{'intent':'','location':'','entities':[] } }
        # TODO: at this moment, all callback assume go for lineResponse
        uid = '' 
        if 'uid' in even :
            uid = even['uid']
        else:
            return 

        print(even)
        keywords = [even['msg']]
        commonRemoves = ['景點','地方','好玩','秘境','私房景點','美食','推薦','旅遊','小姍','哪裡','哪邊','哪有','去哪邊','去哪裡','觀光']
        if 'location' in even['intent'] and even['intent']['location'] != '':
            keywords.append(even['intent']['location'])
        keywords.extend(even['intent']['entities'])
        for r in commonRemoves:
            if r in keywords:
                keywords.remove(r)
        
        print(keywords)
        msg = getTravelNews(keywords)
        toLineResponse={'uid':uid, 'msg':msg}

        print(msg)
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

def lambda_fanshandler(even, context):
    try:
        print("-----In Lambda_fanshandler---")
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
    even = {'uid': 'Uc9b95e58acb9ab8d2948f8ac1ee48fad', 'callback': '', 'botid': '', 'msg': '小姍推薦日本高山景點', 'intent': {'timings': [], 'entities': ['小姍', '景點','觀光'], 'msg': '小姍推薦日本觀光景點', 'location': '日本', 'intent': '推薦'}}
    

#    lambda_foodhandler(even, None)
    lambda_travelhandler(even,None)
