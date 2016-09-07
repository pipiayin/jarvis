#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from datetime import datetime
import sys
import csv
from awsconfig import ESHOST, REGION

host = ESHOST
region = REGION


#host = 'search-tsai-t5aqxu4dppacep22fq5b4uvj6m.us-east-1.es.amazonaws.com'
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

print("load kb csv file to allkb{}")

allkb = {}
with open(sys.argv[1]) as csvfile:
    slines = csv.reader(csvfile, delimiter=',', quotechar='"')
    for line in slines:
        oriKey = line[0].strip()
        swords = line[1:]
        res = []
        for w in swords:
            w = w.strip()
            if w == '':
                continue
            res.append(w)
        item={u'pkey':oriKey, u'res':res}
        allkb[oriKey] = item
        # to make sure similar table always has itself


print("map similar key word mapping to allkb{}....")

with open(sys.argv[2]) as sfile:
    slines = csv.reader(sfile, delimiter=',', quotechar='"')
    for line in slines:
        oriKey = line[0].strip()
        swords = line[1:]
        similarList = []
        for w in swords:
            w = w.strip()
            if w == '':
                continue
            # build in each word
            toInsert = allkb[oriKey]
            toInsert['similar'] = w
            similarList.append(w)
            print(toInsert)
            res = es.index(index="testi", doc_type='fb',  body=toInsert)

#        if oriKey in allkb:
#            allkb[oriKey]['similar'] = similarList


#for k in allkb:
#    print(allkb[k])
#    #res = es.index(index="testi", doc_type='fb',  body=allkb[k])

es.indices.refresh(index="testi")
print("======= all upload ======")


q = {
      "min_score": 0.9 ,
      "query" :{
      "multi_match" : {
        "query": u'虛擬助理',
        "fields": [ "pkey", "similar" ]
      }
      }
 }



res = es.search(index="testi", body=q)
print(res)
print("Got %d Hits:" % res['hits']['total'])
for h in res['hits']['hits']:
    print(h)


