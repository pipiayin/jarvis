#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#encoding=utf-8

import urllib.request
import json
import requests

wikiAPI = u'https://zh.wikipedia.org/w/api.php?uselang=zh_tw&action=query&prop=extracts&format=xml&exintro=&titles=袋鼠'

#wikiAPI = u'https://zh.wikipedia.org/w/api.php?uselang=zh_tw&action=query&prop=extracts&format=json&exintro=&titles=%E6%BE%B3%E5%A4%A7%E5%88%A9%E4%BA%9E'

#with urllib.request.urlopen(wikiAPI) as response:
#   html = response.read().decode('utf-8')
#   r = json.loads(html)
#   print(r)

r  = requests.get(wikiAPI)

print(r.encoding)
print(dir(r))
print(r.text)

