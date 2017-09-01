#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function


import random
from elasticsearch import Elasticsearch, RequestsHttpConnection
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

def lambda_kbhandler(even, context):
# even structure
# {'msg','' , 'index':'testi',
#  "field":'pkey',"res":"res", 
#  "score":2  } #min_score

    msg = even['msg']
    field = even['field']
    idx = even['index']
    if "score" in even:
        min_score = int(even['score'])

    q = {
      "min_score": min_score,
      "query" :{
      "multi_match" : {
        "query": msg, 
        "fields": [ field]
      }
      }
    }   

    res = es.search(index=idx, body=q)
    print("Got %d Hits:" % res['hits']['total'])
    allposi =[]
    allposiScore =[]
    cntPossible = 0
    for h in res['hits']['hits']:
        #print(h)
        score = int(h['_score'])+1
        allposi = allposi + h['_source']['res']
        allposiScore.append(score)
        cntPossible += 1
        #result = random.choice((h['_source']['res']))
        #return result
    toPick = []
    for exdi in range(cntPossible):
        toPick = toPick + [exdi] * allposiScore[exdi]
    #print(toPick)
    if len(allposi) > 0:
        resultPick = random.choice(toPick)
        result = allposi[resultPick]
        return result

    return ""

if __name__ == '__main__':

    import sys
    msg = sys.argv[1]
    even = {'msg':msg , 'index':'testi', "field":'pkey',"res":"res", "score":2.1  } 
    r = lambda_kbhandler(even, None)
    print("==== result ===")
    print(r)


