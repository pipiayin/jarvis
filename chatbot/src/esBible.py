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
from awsconfig import ESHOST

host = ESHOST

min_score=1.2

aws_access_key_id = ''
aws_secret_access_key = ''

#es = Elasticsearch( hosts=[{'host': host, 'port': 443}])
#es = Elasticsearch(host=host, port=80)

awsauthfile = 'credentials'
with open(awsauthfile) as f:
    content = f.readlines()
    for line in content:
        if 'aws_access_key_id' in line :
            aws_access_key_id = line.split("=")[1].strip()
        if 'aws_secret_access_key' in line :
            aws_secret_access_key = line.split("=")[1].strip()

awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, 'us-east-1', 'es')

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

def preProcess(msg):
    cList = ['不知道該怎麼辦','怎麼辦','?','？',"。","，",":",";"]
    for c in cList:   
        if msg.count(c) > 0:
            msg = msg.replace(c," ")
    return msg


def esBibleHandler(msg, words):
    result =""
    msg = preProcess(msg)

    q = {
      "min_score": min_score,
      "query" :{
      "match" : {
        "text": msg
      }
      }
    }   


    res = es.search(index="bible", body=q)
    print("Got %d Hits:" % res['hits']['total'])
    # find 3 hits max
    maxhit = 3
    cnt = 1
    prefix = u'或許你想知道的是基督信仰方面...\n'
    for h in res['hits']['hits']:
        result = result + (h['_source']['text'])+ " \n"
        #result = extraFilter(result)
        cnt +=1
        if cnt > maxhit:
            break
    if result != '':
        result = prefix+result
    return result


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("usage: python "+sys.argv[0]+" <keyword> ")
        print("")
        exit(0)


    print("==== result ===")
    print(esBibleHandler(sys.argv[1],[])) 

