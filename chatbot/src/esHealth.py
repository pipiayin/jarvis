#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import sys
import csv
import json
import random
from elasticsearch import Elasticsearch, RequestsHttpConnection
from datetime import datetime
import sys
import csv
from requests_aws4auth import AWS4Auth
from awsconfig import ESHOST, REGION


#host = 'search-sandyai-mdmcmay32zf36sgmk66tz2v454.us-east-1.es.amazonaws.com'
host = ESHOST
region = REGION
min_score=1.2

aws_access_key_id = ''
aws_secret_access_key = ''

#es = Elasticsearch( hosts=[{'host': host, 'port': 443}])
#es = Elasticsearch(host=host, port=80)

awsauthfile = 'credentials_ai'
with open(awsauthfile) as f:
    content = f.readlines()
    for line in content:
        if 'aws_access_key_id' in line :
            aws_access_key_id = line.split("=")[1].strip()
        if 'aws_secret_access_key' in line :
            aws_secret_access_key = line.split("=")[1].strip()

awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, region, 'es')

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
def extraFilter(msg):
    rList = ['您好：','你好:','您好:','你好：','妳好：','妳好:','您好','你好','妳好']

    for r in rList:   
        if msg.count(r) > 0:
            msg = msg.split(r)[-1]
            break

    return msg

def preProcess(msg):
    cList = ['不知道該怎麼辦','怎麼辦','?','？',"。","，",":",";"]
    for c in cList:   
        if msg.count(c) > 0:
            msg = msg.replace(c," ")
    return msg


def esHealthHandler(msg, words,mscore=1.2):
    result =""
    msg = preProcess(msg)

    q = {
      "min_score": mscore,
      "query" :{
      "match" : {
        "q": msg
      }
      }
    }   


    res = es.search(index="health", body=q)
    print("Got %d Hits:" % res['hits']['total'])
    for h in res['hits']['hits']:
        result = (h['_source']['a'])
        result = extraFilter(result)
        if mscore >= 0.9:
            result = u'或許健康訊息對你有用唷, 以下資料查詢自台灣e院相關問題回答...\n'+result
        else:
            result = u'小姍猜想可能是問健康問題, 以下資料查詢自台灣e院相關問題回答...\n'+result
        break
    return result


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("usage: python "+sys.argv[0]+" <keyword> ")
        print("")
        exit(0)


    print("==== result ===")
    print(esHealthHandler(sys.argv[1],[])) 

