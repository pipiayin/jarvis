# -*- coding: utf-8 -*-

from __future__ import print_function 
import json
import boto3
import sys
import datetime
from lineEvent import registEvent, unRegistEvent
from boto3.dynamodb.conditions import Key

from difflib import SequenceMatcher



lambda_client = boto3.client('lambda')
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table_event = dynamodb.Table('lineevent')
# TODO a better mapping method
eventMap = {'disweathernotify' :{ 'fuzzy':[
                                u'停止通知我天氣特報',
                                u'停止通知天氣特報',
                                u'不要通知我天氣特報',
                                u'不要通知天氣特報',],
                               'registerMsg' : '好吧 現在開始不會通知你激烈天氣特報',
                               'act' : 'inactive',
                               'callback' : 'weathernotify',
            },
            'weathernotify': { 'fuzzy' : [u'請通知我天氣特報' ,
                                     u'請通知激烈天氣特報',
                                     u'小姍請通知我天氣特報',
                                     u'小姍通知我激烈天氣特報',
                                     u'通知激烈天氣特報',
                                     u'通知天氣特報',
                                    ],
                                'registerMsg' : '小姍會透過中央氣象局的資訊 在有天氣特報時通知您',
                               'act' : 'active',
                               'callback' : 'weathernotify',
                            },
            'dailyenglish': {  'fuzzy' : [u'請每天教我一句英文',
                     u'請給我每日一句學英文',
                     u'小姍請給我每日一句學英文',
                     u'小姍給我每日一句學英文',
                     u'每日一句學英文',
                     u'自動給我每日一句學英文',],
                               'registerMsg' : '小姍每天傍晚會傳一句有深度的英文佳句 讓你每天可以增加自己的英文能力',
                               'act' : 'active',
                               'callback' : 'dailyenglish'
                            },
    
           }
    
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def invokeLineSend(uid, msg):
    toLineResponse={'uid':uid, 'msg':msg}
    lresponse = lambda_client.invoke(
        FunctionName='lineResponse',
        InvocationType='Event',
        LogType='None',
        ClientContext='string',
        Payload=json.dumps(toLineResponse),
    )

def lambda_handler(even, context):
    """ even format: {"uid": "uid": , "evenName":"fuzzy name"}
    """
  #  try:
    print("-----In Lambda_evenreg---")
    fuzzyName = even['evenName'].strip().replace(' ','')
    for k in eventMap:
        for n in eventMap[k]['fuzzy']:
            if similar(n, fuzzyName) > 0.85 :
                act = eventMap[k]['act']
                lambdaName = eventMap[k]['callback']
                if act == 'active' and ('停止' in fuzzyName or '不' in fuzzyName):
                    continue
                if act == 'inactive' and ('停止' not in fuzzyName and '不' not in fuzzyName):
                    #print(fuzzyName +" -->" +act) 
                    
                    continue

                print("to "+act+" "+even['uid']+" in "+k)
                if act == 'inactive' :
                    unRegistEvent(lambdaName, even['uid'])
                    invokeLineSend(even['uid'], eventMap[k]['registerMsg'])
                    return 
                if act == 'active' :
                    registEvent(lambdaName, even['uid'])
                    invokeLineSend(even['uid'], eventMap[k]['registerMsg'])
                    return 

    return 
   # except:
   #     print(even)
   #     print(sys.exc_info()[0])
   #     return "something wrong"
   

if __name__ == '__main__':
    evenName = sys.argv[1]
    even = {'uid': 'Uc9b95e58acb9ab8d2948f8ac1ee48fad','evenName':evenName}
    lambda_handler(even, {})
    print("to register::"+str(even))
    
    #print(getRegisterUsers())
