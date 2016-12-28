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


min_score=0.8

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

def genericHandler(idx, searchq, msg,min_score=0.8):
    
    result =""
    #TODO, remove the assumption of fields q and q and use searchq instead
    q = {
      "min_score": min_score,
      "query" :{
      "multi_match" : {
        "query": msg, 
        "fields": [ "q"  ] 
      }
      }
    }

    print(idx)
    print(q)
    res = es.search(index=idx, body=q)
    hits = res['hits']['total'] 
    print("Got %d Hits:" % res['hits']['total'])
    if hits == 0:
        return ""
    allposi =[]
    cnt = 0
    rDict = random.choice(res['hits']['hits'][:2])
    if type(rDict['_source']['a']) is list:
        result = rDict['_source']['a'][0]
    else:
        result = rDict['_source']['a']
    return result

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("usage: python "+sys.argv[0]+" idx q msg ")
        print("")
        exit(0)


    print("==== result ===")
#    print(genericHandler('bot1', 'q' ,sys.argv[1]))
    print(genericHandler('happyrun', 'q' ,sys.argv[1]))


