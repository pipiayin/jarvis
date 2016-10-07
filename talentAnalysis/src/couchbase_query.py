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

#couchbucket.n1ql_query('CREATE PRIMARY INDEX ON persona').execute()
queryone = couchbucket.get('Alan_Wang@trend.com.tw')

#print(queryone.value)


print("-----by name view----")

cnt = 1
cntnokey = 1
v = View(couchbucket, "byname", "byname",limit=3000)
for r in v:
    theManager =""
    if r.key != None:
        allADdates=[]
        for rk in r.value.keys():
            if rk.startswith('AD'):
                allADdates.append(rk)
               # print(str(allADdates.sort()))

        allADdates.sort()
        for adDay in allADdates:
            if ('manager' in r.value[adDay][1]):
                cnt+=1
                theManager = theManager + " ## "+ r.value[adDay][1]['manager'][0].split(",")[0]

        print(str(r.key)+ " @@@ " +theManager)
    else:
        print("cnt no key="+str(cntnokey))
        cntnokey+=1
#    if cnt >=10:
#        break
print("total cntnokey"+str(cntnokey))



