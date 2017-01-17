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
#host = 'search-sandyai-mdmcmay32zf36sgmk66tz2v454.us-east-1.es.amazonaws.com'

awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, region, 'es')


es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
print(es.info())

def loadToEs(keyfile, csvfile, idx, dtype):
    print("load kb csv file to allkb{}")

    allkb = {}
    with open(keyfile) as kfile:
        slines = csv.reader(kfile, delimiter=',', quotechar='"')
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

    with open(csvfile) as sfile:
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
            res = es.index(index=idx, doc_type=dtype,  body=toInsert)


#es.indices.refresh(index=idx)

    print("======= all uploaded ======")


if __name__ == '__main__':
    import sys


    keyfile = sys.argv[1]
    csvfile = sys.argv[2]
    idx = sys.argv[3]
    dtype = sys.argv[4]
    loadToEs(keyfile,csvfile, idx, dtype)

#res = es.search(index=idx, body=q)
#print(res)
#print("Got %d Hits:" % res['hits']['total'])
#for h in res['hits']['hits']:
#    print(h)


