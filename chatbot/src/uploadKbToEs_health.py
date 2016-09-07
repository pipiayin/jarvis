#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from datetime import datetime
import fileinput

import sys
import csv
from awsconfig import ESHOST, REGION

host = ESHOST
region = REGION

#host = 'search-sandyai-mdmcmay32zf36sgmk66tz2v454.us-east-1.es.amazonaws.com'
awsauthfile = 'credentials_ai'
aws_access_key_id = '' 
aws_secret_access_key = ''

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
print(es.info())

print("to load...")

with open(sys.argv[1]) as f:
    for tmpLine in f:
        line = tmpLine.strip().split(",")
        q = line[0].strip()
        a = line[1].strip()
        dr = line[2].strip()
        item={u'q':q, u'a':a, u'dr':dr}
        # to make sure similar table always has itself

        print(item)
        res = es.index(index="health", doc_type='web',  body=item)

#            allkb[oriKey]['similar'] = similarList


#for k in allkb:
#    print(allkb[k])
#    #res = es.index(index="testi", doc_type='fb',  body=allkb[k])

es.indices.refresh(index="health")
print("======= all upload ======")


q = {
      "query" :{
      "multi_match" : {
        "query": u'心悸',
        "fields": [ "q", "a" ]
      }
      }
 }



res = es.search(index="health", body=q)
print(res)
print("Got %d Hits:" % res['hits']['total'])
for h in res['hits']['hits']:
    print(h)


