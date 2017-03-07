#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from datetime import datetime
import sys
import csv
from awsconfig import ESHOST
from nocheckin import aws_access_key_id,aws_secret_access_key

host = ESHOST


#host = 'search-tsai-t5aqxu4dppacep22fq5b4uvj6m.us-east-1.es.amazonaws.com'

awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, 'us-west-2', 'es')


es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
print(es.info())
es.indices.delete(index="bible")
es.indices.create(index="bible")

print("load kb csv file to allkb{}")

allkb = {}
prefix = u'聖經 '
with open(sys.argv[1]) as bfile:
    slines = csv.reader(bfile, delimiter=' ', quotechar='"')
    for line in slines:
        if line[0] == 'END' or line[0][0] =='=':
            continue 
        #for w in line: 
        #    print(w)
#        oriKey = line[0].strip()
        content = " ".join(line[2:]).replace("\u3000","")
        content = prefix + content 
        subno = prefix + line[2]+" "+line[3]
#        res = []
#        for w in swords:
#            w = w.strip()
#            if w == '':
#                continue
#            res.append(w)
        item={u'text':content, u'sub':subno}
        res = es.index(index="bible", doc_type='web',  body=item)
        print(item)
#        allkb[oriKey] = item
        # to make sure similar table always has itself


print("map similar key word mapping to allkb{}....")

#for k in allkb:
#    print(allkb[k])
#    #res = es.index(index="testi", doc_type='fb',  body=allkb[k])

es.indices.refresh(index="bibile")
print("======= all upload ======")


#q = {
#      "min_score": 0.9 ,
#      "query" :{
#      "multi_match" : {
#        "query": u'虛擬助理',
#        "fields": [ "pkey", "similar" ]
#      }
#      }
# }



#res = es.search(index="testi", body=q)
#print(res)
#print("Got %d Hits:" % res['hits']['total'])
#for h in res['hits']['hits']:
#    print(h)


