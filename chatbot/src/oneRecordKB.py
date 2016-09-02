#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from datetime import datetime
import sys
import csv

#host = 'search-tsai-t5aqxu4dppacep22fq5b4uvj6m.us-east-1.es.amazonaws.com'
host = 'search-sandyai-mdmcmay32zf36sgmk66tz2v454.us-east-1.es.amazonaws.com'
awsauthfile = '/root/.aws/credentials'
aws_access_key_id = '' 
aws_secret_access_key = ''

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
print(es.info())

print("just insert one record")
msg = sys.argv[1]
allres = sys.argv[2]
allres = allres.strip()
res = allres.split(";")

toInsert={u'pkey':msg, u'res':res, u'similar':msg}

res = es.index(index="testi", doc_type='fb',  body=toInsert)


es.indices.refresh(index="testi")
q = {
      "query" :{
      "match" : {
        "similar": msg
      }
      }
 }


res = es.search(index="testi", body=q)
print("Got %d Hits:" % res['hits']['total'])
for h in res['hits']['hits']:
    print(h)


