#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from __future__ import print_function 
from socialBrain import SocialBrain
import json
import boto3
import sys
import json
import time
import random
import botocore.session
import requests

lineBrain = SocialBrain()

def responseToUser(uid, resp):
#    try:
        print("to response to line user")
        headers = {"Content-type": "application/json; charset=utf-8","X-Line-ChannelID" : "1479704687" , "X-Line-ChannelSecret" : "f5e527151c0c039c2f1f41eeb74d3fb0" , "X-Line-Trusted-User-With-ACL" : "ue7f007a54c9cdc5dcd8b0dad74b4e7ad"}
        payload = { 
            "to":[uid],
            "toChannel":1383378250,
            "eventType":"138311608800106203",
            "content":{
                "contentType":1,
                "toType":1,
                "text": resp
             }
        }  

        jdump = json.dumps(payload)
        print(jdump)
        url = 'https://trialbot-api.line.me/v1/events'
        r = requests.post(url, headers=headers, data = jdump)
        print(r)
        print(r.text)
        print("did send response")

        return ''
#    except:
#        return ''
        

def lambda_handler(even, context):
   # try:
        print("-----get message this is lambda brain ---")
        fromuid = even['result'][0]['content']['from']
        msg = even['result'][0]['content']['text']
        resp = lineBrain.think(msg)
        responseToUser(fromuid,resp)
        return "ok"
   # except:
   #     print(even)
   #     print(sys.exc_info()[0])
   #     return "something wrong"
   

if __name__ == '__main__':
    import sys

    msg = sys.argv[1]

    # To try from command line
    tmp = { "result":[ { "from":"u206d25c2ea6bd87c17655609a1c37cb8", "fromChannel":1341301815, "to":["u0cc15697597f61dd8b01cea8b027050e"], "toChannel":1441301333, "eventType":"138311609000106303", "id":"ABCDEF-12345678901", "content":{ } } ] }
    print(lambda_handler(tmp, None))

    
