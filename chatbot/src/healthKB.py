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


min_score=0.9

host = 'search-sandyai-mdmcmay32zf36sgmk66tz2v454.us-east-1.es.amazonaws.com'
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

awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, 'us-east-1', 'es')

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

def extraFilter(msg):
    removeList =[u'您好',u'你好',u'妳好']
    for i in removeList:
        if msg.count(i) >1:
            msg = msg.split(i)[-1]

    return msg

def esHandler(msg, words):
    result =""
    q = {
      "min_score": min_score,
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
        break
    return result


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("usage: python "+sys.argv[0]+" <keyword> ")
        print("")
        exit(0)


    print("==== result ===")
    print(esHandler(sys.argv[1],[]))


