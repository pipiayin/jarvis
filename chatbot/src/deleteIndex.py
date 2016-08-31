#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from datetime import datetime

host = 'search-sandyai-mdmcmay32zf36sgmk66tz2v454.us-east-1.es.amazonaws.com'
awsauth = AWS4Auth('AKIAISA4GAR6JJLA4QNQ', 'towlfkviLmA4QMpMmS3mhBNNdWbsg6yQqyMoUciF', 'us-east-1', 'es')


es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
print(es.info())

#es.indices.refresh(index="testi")


#q = {
#  "query" :{
#  "match" : { '':''
#  }
#  }
#}

#res = es.search(index="testi", body=q)

#print(dir(es))
#print("Got %d Hits:" % res['hits']['total'])
#print(res['hits']['hits'])
print('-----')
es.indices.delete('testi')

