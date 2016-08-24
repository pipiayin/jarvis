#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import json
import requests
import jieba
import jieba.posseg as pseg
import random
import time
import sys
import csv
from dynamoKB import matchHandler
from pttChat import pttHandler


class SocialBrain():
    
    kb = {}
    wikiAPI = u'https://zh.wikipedia.org/w/api.php?uselang=zh_tw&action=query&prop=extracts&format=json&exintro=&redirects=&titles='
    def __init__(self):
        
        with open('basickb.csv') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                if(len(row)>=2):
                    self.kb[row[0].strip()] = row[1].strip()

    def tryExactMatch(self, msg):
        for key in self.kb:
            if msg.count(key) > 0:
                return self.kb[key]
        return ""

    def basicParser(self, msg, words):
        response = ""
        if len(msg) >= 60:
            res_act = self.kb[u'act_too_many_words'].split(";")
            return random.choice(res_act)

#        res_em = self.tryExactMatch(msg)
#        if res_em != '':
#            return res_em

       # print(dir(words))
        return response

    def wikiParser(self, msg, words):
        #print("go to wikiparser??")
        result = ""
        #print(words)
        for word in words:
            if word.flag in ['n','j','x']:
                #print("to find"+str(word))
                wikiResult = self.findWiki(word)
                if wikiResult == '':
                    return result
                else:
                    return wikiResult
            else:
                pass
        return result

    def simpleListWords(self, words):
        toThinkList = []
        for w in words:
            toThinkList.append(w.word)
        return toThinkList

    def think(self, msg):
        response = ""
        handler_list = [self.basicParser, matchHandler, pttHandler]
        words = pseg.cut(msg)
        
        words = self.simpleListWords(words)

        for h in handler_list :
            basic_res = h(msg,words) 
            if basic_res != '':
                return basic_res
         
        if response == '':
            return self.kb['act_no_info']
        else:
            return response

    def findWiki(self, word):
        url = self.wikiAPI+word.word
        #print(url)
        r  = requests.get( self.wikiAPI+word.word )
        return self.getExtract(r.text)

    def getExtract(self, wikiApiRes):
        if wikiApiRes.count('<extract')==0 :
            return ""
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





if __name__ == '__main__':

    fbBrain = SocialBrain()
    msg = sys.argv[1]

    print(fbBrain.think(msg))



