#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#encoding=utf-8

import urllib.request
import json
import requests


def getExtract(wikiApiRes):
    result = wikiApiRes.split('<extract')[1].split('</extract>')[0]
    result = result.replace('xml:space="preserve">','')
    result = result.replace('&lt;','')
    result = result.replace('p&gt;','')
    result = result.replace('/b&gt;','')
    result = result.replace('b&gt;','')
    result = result.replace('/p&gt;','')
    result = result.replace('&gt;','')
    result = result.replace('br&gt;','')

    return result


wikiAPI = u'https://zh.wikipedia.org/w/api.php?uselang=zh_tw&action=query&prop=extracts&format=xml&exintro=&titles=孫中山'

#wikiAPI = u'https://zh.wikipedia.org/w/api.php?uselang=zh_tw&action=query&prop=extracts&format=json&exintro=&titles=%E6%BE%B3%E5%A4%A7%E5%88%A9%E4%BA%9E'

#with urllib.request.urlopen(wikiAPI) as response:
#   html = response.read().decode('utf-8')
#   r = json.loads(html)
#   print(r)

r  = requests.get(wikiAPI)

print(r.encoding)
print(dir(r))
print(getExtract(r.text))

