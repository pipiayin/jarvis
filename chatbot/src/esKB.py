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
from nocheckin import aws_access_key_id,aws_secret_access_key


min_score=2

#host = 'search-sandyai-mdmcmay32zf36sgmk66tz2v454.us-east-1.es.amazonaws.com'
host = ESHOST
region = REGION

#es = Elasticsearch( hosts=[{'host': host, 'port': 443}])
#es = Elasticsearch(host=host, port=80)

awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, region, 'es')

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

def esHandler(msg, words):
    result =""

    q = {
      "min_score": min_score,
      "query" :{
      "multi_match" : {
        "query": msg, 
        "fields": [ "pkey", "similar" ] 
      }
      }
    }   

    res = es.search(index="testi", body=q)
    print("Got %d Hits:" % res['hits']['total'])
    allposi =[]
    for h in res['hits']['hits']:
        allposi = allposi + h['_source']['res']
        #result = random.choice((h['_source']['res']))
        #return result
    if len(allposi) > 0:
        result = random.choice(allposi)
        return result

    qb = {
      "min_score": 1.2,
      "query" :{
      "multi_match" : {
        "query": msg, 
        "fields": [ "pkey"]
      }
      }
    }   

    res = es.search(index="books1", body=qb)
    print("Got %d Hits:" % res['hits']['total'])
    if len(res['hits']['hits']) == 0:
        return ''
    else:
   #     for i in res['hits']['hits']:
   #         print(i['_source']['res'])
        resultDict = random.choice(res['hits']['hits'][:3])
        result = resultDict['_source']['res']
        return result

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("usage: python "+sys.argv[0]+" <keyword> ")
        print("")
        exit(0)


    print("==== result ===")
    print(esHandler(sys.argv[1],[]))


