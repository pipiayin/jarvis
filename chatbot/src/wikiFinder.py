#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Just a tool to find a word from wiki

import json
import requests
import sys
import re

def findWiki( word):
    url = u'https://zh.wikipedia.org/w/api.php?uselang=zh_tw&action=query&prop=extracts&format=xml&exintro=&redirects=&titles={0}'
    r  = requests.get(url.format(word) )
    result = getExtract(r.text)
    #print(result)
    if result.count(u'簡繁重定向')>0:
        result = ''
    return result

def findWikiEn(word):
    url = u'https://en.wikipedia.org/w/api.php?uselang=en_US&action=query&prop=extracts&format=xml&exintro=&redirects=&titles={0}'
    r  = requests.get(url.format(word) )
    result = getExtract(r.text)
    return result

def getExtract( wikiApiRes):
    if wikiApiRes.count('<extract')==0 :
        return ""
    #result = wikiApiRes.split('<extract')[1].split('</extract>')[0]
    result = wikiApiRes.strip()

    result = re.sub(r'\<.*?\>', '', result)
    result = re.sub(r'（.*?）', '', result)
    result = re.sub(r'\(.*?\)', '', result)
    result = re.sub(r'（.*?）', '', result)
    result = re.sub(r'\&lt;.*?\&gt;', '', result)
    result = re.sub(r'\n', '', result)
#    ignoreList = ['xml:space="preserve">','&lt;','p&gt;','/b&gt;','b&gt;','/p&gt;','&gt;','br&gt;']
#    for i in ignoreList:
#        result = result.replace(i,'')
    return result


if __name__ == '__main__':

    msg = sys.argv[1]

    print(findWikiEn(msg))
    
