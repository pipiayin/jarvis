#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from datetime import datetime
import sys
import csv
from nocheckin import aws_access_key_id,aws_secret_access_key

#麼麼host = 'search-tsai-t5aqxu4dppacep22fq5b4uvj6m.us-east-1.es.amazonaws.com'
host = 'search-sandy4ai-smzneodznkksyveysvwd6c456a.us-west-2.es.amazonaws.com'

#host = 'search-sandyai-mdmcmay32zf36sgmk66tz2v454.us-east-1.es.amazonaws.com'
awsauthfile = 'credentials_ai'


awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, 'us-west-2', 'es')


es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
print(es.info())

idx = sys.argv[1]
#es.indices.delete(index=idx)
es.indices.create(index=idx)
print("======= all remove? ======")




