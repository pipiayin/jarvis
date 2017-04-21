#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import json
import requests
import sys
import jieba
import jieba.posseg as pseg
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

def wikiHandler(msg, words):

    #TODO for wiki handler, need to use jieba to parse string again. 
    # could be improve in the future
    wikiResult =''
    try:
        if len(msg) <= 4: ## short message
            wikiResult = findWiki(msg)
            wikiResult = shortenResult(wikiResult)
            if wikiResult != '':
                return wikiResult
            
        jieba.load_userdict('data/dict.txt.big')
        words = pseg.cut(msg)
        tWord = ''
        for word in words:
            #print("debug:: "+str(word.word)+ " "+str(word.flag))
            if word.flag in ['n','j','nr','ns','nt','an','nt']:
                tWord = tWord + str(word.word)
                print("to find "+ tWord)
                    #print("yes")
               
            else:
                tWord = tWord+"!"
             
        print(tWord)
        tmpL = tWord.split("!")
        allList = list(set(tmpL))
        #print(allList)
        if u'' in allList:
            allList.remove(u'')
        if len(allList) == 0:
            #means no need to find
            return ''
        
        tWord = allList[0].strip() #just pick first
        if len(tWord) <= 1:
            print('avoid one sinegle chinese char search')
            return ''

        print("find "+tWord)
        wikiResult = findWiki(tWord)
        wikiResult = shortenResult(wikiResult)

        if len(allList) >= 2 and wikiResult =='': # give the string second chance
            tWord = allList[1].strip() #just pick first
            print("find second term "+tWord)
            wikiResult = findWiki(tWord)
            wikiResult = shortenResult(wikiResult)

        return wikiResult
    except: 
        print(sys.exc_info()[0])
        return 'err'

    return wikiResult
if __name__ == '__main__':

    msg = sys.argv[1]

    print(wikiHandler(msg,[]))
    #
