#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
import lxml.html as lh
#from StringIO import StringIO
from io import StringIO
import re

from lxml import etree

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from datetime import datetime
import sys
import csv

#host = 'search-tsai-t5aqxu4dppacep22fq5b4uvj6m.us-east-1.es.amazonaws.com'
host = 'search-sandyai-mdmcmay32zf36sgmk66tz2v454.us-east-1.es.amazonaws.com'
awsauthfile = '/root/.aws/credentials'
aws_access_key_id = '' 
aws_secret_access_key = ''

with open(awsauthfile) as f:
    content = f.readlines()
    for line in content:
        if 'aws_access_key_id' in line :
            aws_access_key_id = line.split("=")[1].strip()
        if 'aws_secret_access_key' in line :
            aws_secret_access_key = line.split("=")[1].strip()

awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, 'us-east-1', 'es')


es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)




def insertEs(doc):
    print('start to insert------------')
    print(doc['dr'])
    res = es.index(index="health", doc_type='web',  body=doc)
    print(res)
    print("inserted ------------")



def basicClean(amsg):
    amsg= amsg.encode('utf-8').strip()
    #print(amsg)
   # amsg= amsg.encode('utf-8').strip()
    amsg = amsg.replace('《','')
    amsg = re.sub(r'\n', '', amsg)
    amsg = re.sub(r'\r', '', amsg)
   # amsg = re.sub(r'\r\n', '', amsg)
    amsg = re.sub(r',', '', amsg)
    amsg = re.sub(r'《', '', amsg)
    amsg = re.sub(r' ', '', amsg)
    r = amsg
    print(r)
    print('done cleaning')
    return r

f = open('health1.csv','a')
for i in range(10121,20000):
    try:
        url='http://sp1.hso.mohw.gov.tw/doctor/All/ShowDetail.php?q_no='
        r = requests.get(url+str(i))
#    print(r.status_code)
        htmlstr = r.text.encode('latin1', 'ignore').decode('big5')
        if htmlstr.count(u'不存在</h1>'):
            print('ignore '+str(i))
            continue
    #doc=lh.parse(htmlstr)
        parser = etree.HTMLParser()
        sio = StringIO(htmlstr)
        tree = etree.parse(StringIO(htmlstr), parser)
        question = tree.find(".//li[@class='ask']")
        allq =""
        for t in question.itertext():
            allq = allq + t
        dr = tree.find(".//li[@class='doctor']").text
#    dr.nsplit(",")[0]
        ans = tree.find(".//li[@class='ans']")
        alla = ""
        for t in ans.itertext():
            t.replace("\n","")
            alla = alla+t
    
        allq = basicClean(allq)
        alla = basicClean(alla)
        dr = basicClean(dr)
        oneresult = {'a':alla,'q':allq,'dr':dr}
#        insertEs(oneresult)
        f.write(allq+ ","+alla+","+dr)
        f.write("\n")
    except:
        print(sys.exc_info()[0])
        pass 

es.indices.refresh(index="health")
#    print(oneresult)
#    print(r.text.encode('utf-8'))
f.flush()
f.close()
