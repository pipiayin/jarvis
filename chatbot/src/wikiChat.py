#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import json
import requests
import sys
import jieba
import jieba.posseg as pseg
import re

def findWiki( word):
    url = u'https://zh.wikipedia.org/w/api.php?uselang=zh_tw&action=query&prop=extracts&format=xml&exintro=&titles={0}'
    r  = requests.get(url.format(word) )
    result = getExtract(r.text)
    if result.count(u'簡繁重定向')>0:
        result = ''
    return result

def getExtract( wikiApiRes):
    if wikiApiRes.count('<extract')==0 :
        return ""
    result = wikiApiRes.split('<extract')[1].split('</extract>')[0]
    ignoreList = ['xml:space="preserve">','&lt;','p&gt;','/b&gt;','b&gt;','/p&gt;','&gt;','br&gt;']
    for i in ignoreList:
        result = result.replace(i,'')

    result = re.sub(r'\<.*?\>', '', result)
    result = re.sub(r'\(.*?\)', '', result)
    result = re.sub(r'（.*?）', '', result)
    return result


def wikiHandler(msg, words):

    #TODO for wiki handler, need to use jieba to parse string again. 
    # could be improve in the future
    wikiResult =''
    try:
        jieba.load_userdict('data/dict.txt.big')
        words = pseg.cut(msg)
        for word in words:
            if word.flag in ['n','j','nr','ns','nt','an']:
                print("to find"+str(word))
                wikiResult = findWiki(word.word)
                if len(wikiResult) >= 61 :
                    wikiResult = wikiResult[:60]
                    wikiResult = wikiResult+" ..."
                break
            else:
                print("to ignore"+str(word))
    except: 
        return ''

    return wikiResult
if __name__ == '__main__':

    msg = sys.argv[1]

    print(wikiHandler(msg,[]))
    
