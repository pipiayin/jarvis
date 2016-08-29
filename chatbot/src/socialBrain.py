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
from esKB import esHandler
from pttChat import pttHandler
from wikiChat import wikiHandler


class SocialBrain():
    
    kb = {}
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
        msg = msg.strip() 
        if len(msg) <= 3 and msg in self.kb[u'list_hello'].split(';'): # small lines
            res_act = self.kb[u'act_hello'].split(";")
            return random.choice(res_act)

        if len(msg) >= 60:
            res_act = self.kb[u'act_too_many_words'].split(";")
            return random.choice(res_act)

#        res_em = self.tryExactMatch(msg)
#        if res_em != '':
#            return res_em

       # print(dir(words))
        return response


    def simpleListWords(self, words):
        toThinkList = []
        wordtypes = []
        for w in words:
            toThinkList.append(w.word)
            wordtypes.append((w.word, w.flag))
        return toThinkList, wordtypes

    def think(self, msg):
        response = ""
        all_list = [self.basicParser, esHandler,wikiHandler]
        short_list = [self.basicParser, esHandler]
        handler_list = short_list
        words = pseg.cut(msg)
        
        words, wordtypes = self.simpleListWords(words)
        wcount = len(wordtypes)
        nounwcount = 0.0
        for (w,f) in wordtypes:
            if f in['n','j','nr','ns','nt','an']:
                nounwcount += 1
        if nounwcount / float(wcount) >= 0.29:
            handler_list = all_list 

        for h in handler_list :
            basic_res = h(msg,words) 
            if basic_res != '':
                return basic_res
         
        if response == '': # can't find any answer give 50% for pttHandler
            if random.randint(0,1) == 1:
                response = pttHandler(msg, words)
                if response == '':
                    noInfoList = self.kb['act_no_info'].split(";")
                    response = random.choice(noInfoList)
            return response 
        else:
            return response






if __name__ == '__main__':

    fbBrain = SocialBrain()
    msg = sys.argv[1]

    print(fbBrain.think(msg))



