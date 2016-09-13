#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from datetime import datetime
import sys
import csv
import re
from awsconfig import ESHOST
from nocheckin import aws_access_key_id, aws_secret_access_key

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
#print(es.info())
#es.indices.delete(index="bible")
#es.indices.create(index="books1")

print("load book")

sp = [u'。',u'？',u'！']
ssp = [u'，']
with open(sys.argv[1]) as bfile:
    for line in bfile:
        line = line.strip()
        line = line.replace(' ','')
        if line =='':
            continue
        sects =  re.split(u'。|？|！',line)
        if '' in sects :
            sects.remove('')
        if len(sects) <= 1:
            continue 
        for s in  sects: 
            parts = re.split(u'，',s) 
            mergeTmp = ''
            for key in parts:
                if len(key+u'，'+mergeTmp) >10:
                    resp = "，".join(sects)
                    if resp.replace(' ','') == '':
                        continue
                    item={u'pkey':mergeTmp+u'，'+key, u'res':resp}
                    print(item)
                    mergeTmp = ''
                else:
                    mergeTmp = mergeTmp +u'，'+ key

#                    res = es.index(index="books1", doc_type='web',  body=item)
#        print(item)
#        allkb[oriKey] = item
        # to make sure similar table always has itself
#es.indices.refresh(index="books1")
print("======= all upload ======")

