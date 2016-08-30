#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
import lxml.html as lh
from StringIO import StringIO
import re


from lxml import etree

f = open('out1.csv','a')
for i in range(2,10000):
    try:
        url='http://sp1.hso.mohw.gov.tw/doctor/All/ShowDetail.php?q_no='
        r = requests.get(url+str(i))
#    print(r.status_code)
        htmlstr = r.text.encode('latin1', 'ignore').decode('big5')
        if htmlstr.count(u'不存在</h1>'):
#            print('ignore '+str(i))
            continue
    #doc=lh.parse(htmlstr)
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(htmlstr), parser)
        question = tree.find(".//li[@class='ask']")
        allq =""
        for t in question.itertext():
            allq = allq + t
        print("---")
        print(allq)
        print("---")
        dr = tree.find(".//li[@class='doctor']").text
#    dr.split(",")[0]
        ans = tree.find(".//li[@class='ans']")
        alla = ""
        for t in ans.itertext():
            t.replace("\n","")
            alla = alla+t

        allq = re.sub(r'\n', '', allq)
        alla = re.sub(r'\n', '', alla)
        dr = re.sub(r'\n', '', dr)
    
        allq = re.sub(r',', '', allq)
        alla = re.sub(r',', '', alla)
        dr = re.sub(r',', '', dr)
        print('===========')    
        allq = allq.encode('utf-8').strip()
        alla = alla.encode('utf-8').strip()
        dr = dr.encode('utf-8').strip()
        print('q:'+allq)
        print('a:'+alla)
        print('dr:'+dr)
        print("======")
        oneresult = allq+","+alla+","+dr
    
        f.write(oneresult+"\n")
    except:
        pass 
#    print(oneresult)
#    print(r.text.encode('utf-8'))
