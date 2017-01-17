#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from datetime import datetime
import sys
import csv
from awsconfig import ESHOST, REGION
from nocheckin import aws_access_key_id,aws_secret_access_key

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

def loadToEs( csvfile, idx, dtype):
    print("load kb csv file to allkb{}")


    with open(csvfile) as sfile:
        slines = csv.reader(sfile, delimiter=',', quotechar='"')
        for line in slines:
            q = line[0].strip()
            a = line[1:]
            # build in each word
            toInsert = {u'q':q , u'a':a}
            print(toInsert)
            res = es.index(index=idx, doc_type=dtype,  body=toInsert)


    es.indices.refresh(index=idx)

    print("======= all uploaded ======")


if __name__ == '__main__':
    import sys
    csvfile = sys.argv[1]
    idx = sys.argv[2]
    es.indices.delete(index=idx)
    es.indices.create(index=idx)
    dtype = sys.argv[3]
    loadToEs(csvfile, idx, dtype)
    es.indices.refresh(index=idx)

#res = es.search(index=idx, body=q)
#print(res)
#print("Got %d Hits:" % res['hits']['total'])
#for h in res['hits']['hits']:
#    print(h)


