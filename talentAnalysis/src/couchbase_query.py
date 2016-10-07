#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib


import os
from couchbase import Couchbase
from couchbase.views.iterator import View
from couchbase.n1ql import N1QLQuery
couchbase_host='10.1.193.189'
couchbase_bucket='persona'

 
# Define variables
 
couchbucket = Couchbase.connect(bucket=couchbase_bucket, host=couchbase_host)
print(couchbucket)
#
#couchbucket.n1ql_query('CREATE PRIMARY INDEX ON persona').execute()
queryone = couchbucket.get('Aaron Chu (RD-TW)')

for k in queryone.value:
    print(k)



