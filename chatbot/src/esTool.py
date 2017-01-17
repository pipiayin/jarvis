#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from datetime import datetime
import sys
import csv
from awsconfig import ESHOST, REGION
from nocheckin import aws_access_key_id, aws_secret_access_key

host = ESHOST
region = REGION

#host = 'search-tsai-t5aqxu4dppacep22fq5b4uvj6m.us-east-1.es.amazonaws.com'

awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key,region, 'es')

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
print(es.info())

#es.indices.create(index="health")
#print("======= all upload ======")

msg = sys.argv[3]
field = sys.argv[2]
indexname = sys.argv[1]
q = {
      "query" :{
      "match" : {
        field: msg
      }
      }
 }
q = {
      "min_score": 0.0000001,
      "query" :{
          "match_all" : {
          } 
      },
      "size": 5000
 }

#q = {
#      "min_score": 1,
#      "query" :{
#      "multi_match" : {
#        "query": msg,
#        "fields": [ "pkey", "similar" ]
#      }
#      }
#}

es.indices.refresh(index=indexname)
res = es.search(index=indexname, body=q)
#print(res)
print("Got %d Hits:" % res['hits']['total'])
for h in res['hits']['hits']:
    print(h['_source'])

