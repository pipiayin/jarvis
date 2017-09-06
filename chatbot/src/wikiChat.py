#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import json
import requests
import sys
#import jieba
#import jieba.posseg as pseg
import re

def findWiki( word):
    url = u'https://zh.wikipedia.org/w/api.php?uselang=zh-tw&action=query&prop=extracts&format=xml&exintro=&redirects=&titles={0}'
    r  = requests.get(url.format(word) )
    result = getExtract(r.text)
    #print(result)
    if result.count(u'簡繁重定向')>0:
        result = ''
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

def shortenResult(wikiResult):
   
    if len(wikiResult) >= 200 :
        wikiResult = wikiResult[:200]
        wikiResult = wikiResult+u'...其他可以查一下wiki唷'
    return wikiResult

def wikiHandler(msg, typeWords):

    wikiResult =''
    try:
        if len(msg) <= 4: ## short message
            wikiResult = findWiki(msg)
            wikiResult = shortenResult(wikiResult)
            if wikiResult != '':
                return wikiResult
            
        tWords = []
        tmpWord = ''
        for (flag, word) in typeWords:
            #print("debug:: "+str(word.word)+ " "+str(word.flag))
            if flag in ['n','j','nr','ns','nt','an','nt']:
                tmpWord = tmpWord + str(word)
                tWords.append(tmpWord)
                tWords.append(word)
                print("add to find "+ tmpWord)
                print("add to find "+ word)
                    #print("yes")
             
        allList = list(set(tWords))
        if u'' in allList:
            allList.remove(u'')
        if len(allList) == 0:
            #means no need to find
            return ''
        
        wikiResultList = []
        result = ""
        for targetWord in allList: 
            wikiResult = ''
            if len(targetWord) <= 1:
                continue 
            print("try to find from wiki "+targetWord)
            wikiResult = findWiki(targetWord)
            wikiResult = shortenResult(wikiResult)
            wikiResultList.append(wikiResult)
            print(wikiResult)

        for r in wikiResultList:
            if r.strip() != '' and len(r.strip()) > 0:
                result = result + r + "\n"
            
        return result
    except: 
        print(sys.exc_info()[0])
        return 'err'

if __name__ == '__main__':

    msg = sys.argv[1]
    from twMessageProcess import  getIntent
    intent = getIntent(msg)

    r = wikiHandler(msg,intent['oriCut'])
    print("the result of wikihanlder")
    print(r)
    print("end of result of wikihandler")
    #
