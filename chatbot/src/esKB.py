#!/usr/bin/env python3
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


min_score=1.5

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
    allposiScore =[]
    cntPossible = 0
    pScore = 0 
    for h in res['hits']['hits']:
        #print(h)
        score = int(h['_score'])+1
            
        if pScore != 0 :
            pGap = ( pScore - score) / score 
    #        print(pGap)
            if pGap >= 0.33 :
                break
        pScore = score
        allposi = allposi + h['_source']['res']
        allposiScore.append(score)
        cntPossible += 1
        
        #result = random.choice((h['_source']['res']))
        #return result
    toPick = []
    for exdi in range(cntPossible):
        toPick = toPick + [exdi] * allposiScore[exdi]
    #print(toPick)
    #print(allposi)
    if len(allposi) > 0:
        resultPick = random.choice(toPick)
        result = allposi[resultPick]
        return result

    qb = {
      "min_score": 1.5, # well...books kb score should be higher? anyway...require refactorying in this part
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
        if type(resultDict['_source']['res']) == type([]):
            result = random.choice(resultDict['_source']['res'])
        else:
            result = resultDict['_source']['res']
        return result

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("usage: python3 "+sys.argv[0]+" <keyword> ")
        print("")
        exit(0)


    print("==== result ===")
    print(esHandler(sys.argv[1],[]))


