#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import json
import requests
import jieba
import jieba.posseg as pseg
import re
import random
import time
import sys
import csv
from esKB import esHandler
from esHealth import esHealthHandler
from esBible import esBibleHandler
#from pttChat import pttHandler
from wikiChat import wikiHandler


class SocialBrain():
    
    kb = {}
    processmsg = ''
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

    def randomAct(self, actKey):
        res_act = self.kb[actKey].split(";")
        return random.choice(res_act)
       
    def basicParser(self, msg, words):
        response = ""
        msg = msg.strip() 
        msg = re.sub(u'[~～#$]', '', msg)
        lenMsg = len(msg)
        if lenMsg <= 5 and msg in self.kb[u'list_hello'].split(';'): # small lines
            return self.randomAct(u'act_hello')

        if lenMsg <= 5 and msg in self.kb[u'list_done'].split(';'): # small lines
            return self.randomAct(u'act_ack')

        if lenMsg <= 5 and msg in self.kb[u'list_no'].split(';'): # small lines
            return self.randomAct(u'act_ack_no')

        if lenMsg == 1 : # one words
            return self.randomAct(u'act_one_words')

        if lenMsg == 2 : # two words
            return self.randomAct(u'act_two_words')

        if lenMsg == 3 : # two words
            list3words = self.kb[u'list_three_words'].split(';')
            for tw in list3words:
                if tw == msg:
                    return self.randomAct(u'act_three_words')

        if lenMsg > 9 :
            engcounts = len(re.findall('[a-zA-Z]',msg))
            noMeanCounts = len(re.findall('[ .?!-~]',msg))
            if float(engcounts) / (lenMsg - noMeanCounts) > 0.75:
                return self.randomAct(u'act_no_english')

                
        if lenMsg >= 90:
            return self.randomAct(u'act_too_many_words')
        #### prefix checking

        prefixCheckList = ['']
        # if no return yet. will modify self.processmsg
        # remove what_is and how_to
        toRemoveList =['what_is','how_to']
        for t in toRemoveList :
            rlist = self.kb[t].split(";") 
            for r in rlist:
                self.processmsg = self.processmsg.replace(r," ")
        
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
        self.processmsg = msg # supposedly, basicParser will change processmsg
        all_list = [self.basicParser, esHandler, wikiHandler,esHealthHandler, esBibleHandler]
        short_list = [self.basicParser, esHandler]
        bible_first_list = [self.basicParser, esHandler,esBibleHandler]
        # TODO should have abetter way
        handler_list = short_list
        bList = [u'聖經',u'信仰',u'基督教',u'基督']
        for bw in bList:
            if self.processmsg.count(bw) > 0:
                handler_list = bible_first_list
                break
        words = pseg.cut(msg)
        
        words, wordtypes = self.simpleListWords(words)
        wcount = len(wordtypes)
        nounwcount = 0.0
        for (w,f) in wordtypes:
            if f in['n','j','nr','ns','nt','an','nt']:
                nounwcount += len(w)

        if nounwcount / float(wcount) >= 0.3:
            if wikiHandler not in handler_list:
                handler_list.append(wikiHandler)

        if esHealthHandler not in handler_list:
            handler_list.append(esHealthHandler)
    
        for h in handler_list :
            basic_res = h(self.processmsg,words) 
            #print('handle by'+str(h))
            if basic_res != '':
                return basic_res
         
        if response == '': # can't find any answer give 66% for BibleHandler
            if random.randint(0,2) < 2:
                response = esBibleHandler(msg, words)

#        if response == '': # can't find any answer give 50% for pttHandler
#            if random.randint(0,1) < 1:
#                response = pttHandler(msg, words)

        if response == '':
            noInfoList = self.kb['act_no_info'].split(";")
            response = random.choice(noInfoList)
        return response





fbBrain = SocialBrain()
if __name__ == '__main__':

    msg = sys.argv[1]

    print(fbBrain.think(msg))



