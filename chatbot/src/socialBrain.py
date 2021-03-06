#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import json
import requests
#import jieba
#import jieba.posseg as pseg
import re
import random
import time
import sys
import csv
from esKB import esHandler
from genericKB import genericHandler
from esHealth import esHealthHandler
from esBible import esBibleHandler
#from io import open
import codecs
from pttChat import pttHandler
from wikiChat import wikiHandler

    
class GenericBrain():
    idx = ''
    searchq = ''
    no_res = 'bot_cannot_response'

    kb = {}

    def __init__(self, idx, searchq):
        self.idx = idx
        self.searchq = searchq
        with open('basickb.csv') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                if(len(row)>=2):
                    self.kb[row[0].strip()] = row[1].strip()

    def randomAct(self, actKey):
        res_act = self.kb[actKey].split(";")
        return random.choice(res_act)

    def think(self, intent):
        msg = intent['msg'].strip()
        if msg in self.kb[u'bad_words'].split(';'):
            response = self.randomAct(u'bad_words_res')
            return response

        if msg in self.kb[u'command'].split(';'):
            response = self.randomAct(u'command_res')
            return response
       
        response = genericHandler(self.idx,self.searchq ,msg)
        if response == '':
            response = genericHandler(self.idx,self.searchq ,self.no_res)
 
        if response == '':
            response = self.randomAct(u'happyrun_no_res')

        return response
        

class SocialBrain():
    
    kb = {}
    processmsg = ''
    notFoundResList = []

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
        #msg = msg.encode('utf-8')
        msg = msg.strip()
        msg = re.sub(u'[~～#$]', '', msg)
        lenMsg = len(msg)
        if msg in self.kb[u'command'].split(';'):
            response = self.randomAct(u'command_res')
            return response

        if lenMsg <= 5 and msg in self.kb[u'list_hello'].split(';'): # small lines
            return self.randomAct(u'act_hello')

        if lenMsg <= 5 and msg in self.kb[u'list_done'].split(';'): # small lines
            return self.randomAct(u'act_ack')

        if lenMsg <= 5 and msg in self.kb[u'list_no'].split(';'): # small lines
            return self.randomAct(u'act_ack_no')

        if lenMsg == 1 : # one words
            return self.randomAct(u'act_one_words')

#        if lenMsg == 2 : # two words
#            return self.randomAct(u'act_two_words')

#        if lenMsg == 3 : # two words
#            list3words = self.kb[u'list_three_words'].split(';')
#            for tw in list3words:
#                if tw == msg:
#                    return self.randomAct(u'act_three_words')

        if lenMsg > 9 :
            engcounts = len(re.findall('[a-zA-Z]',msg))
            noMeanCounts = len(re.findall('[ .?!-~]',msg))
            if float(engcounts) / (lenMsg - noMeanCounts+0.1 ) > 0.75:
                return self.randomAct(u'act_no_english')

                
        if lenMsg >= 90:
            return self.randomAct(u'act_too_many_words')
        #### prefix checking

        prefixCheckList = ['']
        # if no return yet. will modify self.processmsg
        # remove what_is and how_to
        notFoundResList = { 'what_is':'what_is_res',
                            'how_to':'how_to_res',
                            'where_is':'where_is_res',
                            'list_tell_me':'list_tell_me_res',
                            'who_is':'who_is_res'}

        for sec in notFoundResList:
            rlist = self.kb[sec].split(";") 
            directBreak = False
            for r in rlist:
                if self.processmsg.count(r) > 0:
                    self.notFoundResList = self.kb[notFoundResList[sec]].split(";")
                    directBreak = True
                    break

            if directBreak:
                break
        
#        res_em = self.tryExactMatch(msg)
#        if res_em != '':
#            return res_em

       # print(dir(words))
        return response


    def simpleListWords(self, oriCut):
        wordtypes = []
        for f,w in oriCut:
            wordtypes.append((w, f))
        return wordtypes

    def think(self, intent):
        msg = intent['msg'].strip()
        response = ""
        self.processmsg = msg # supposedly, basicParser will change processmsg
        all_list = [self.basicParser, esHandler, wikiHandler,esHealthHandler]
        #all_list = [self.basicParser, esHandler, wikiHandler,esHealthHandler, esBibleHandler]
        short_list = [self.basicParser, esHandler]
        #bible_first_list = [self.basicParser, esHandler,esBibleHandler]
        handler_list = short_list
       # bList = [u'聖經',u'信仰',u'基督教',u'基督']
       # for bw in bList:
       #     if self.processmsg.count(bw) > 0:
       #         handler_list = bible_first_list
       #         break
        msg = msg.strip().replace("?",'').replace("？","")
        #words = pseg.cut(msg)
        typeWords = intent['oriCut']
        wcount = len(typeWords)
        nounwcount = 0.0
        ncount = 0
        ncnt = 0
        toCommand = False
        nounWords = []
        toCmdAct = ''
        if msg in self.kb[u'bad_words'].split(';'):
            response = self.randomAct(u'bad_words_res')
            return response

        for (f, w) in typeWords:
            #print("word:"+ w)
            #print("flag:"+f)
            if ncnt == 0 and f in ['v']:
                toCommand = True
            if ncnt > 0 and toCommand and f in ['v'] and toCmdAct == '':
                toCmdAct = w
            if f in['n','j','nr','ns','nt','an','nt']:
                nounwcount += len(w)
                ncount +=1
                nounWords.append(w)
            ncnt += 1

        if wcount == 0:
            wcount = 0.5
        nrate = nounwcount / float(wcount)

        howtolist = self.kb['how_to'].split(";") 
        for howto in howtolist:
            if self.processmsg.count(howto) > 0 and len(self.processmsg) > 6:
                handler_list.append(esHealthHandler)
                break
        whatislist = self.kb['what_is'].split(";")
        whoislist = self.kb['who_is'].split(";")
        whatislist.extend(whoislist)
        for whatis in whatislist:              
            if wikiHandler not in handler_list and self.processmsg.count(whatis) > 0 and nrate >0.3 :
                #print("add to what/who is")
                handler_list.append(wikiHandler)
                break

        if wcount <=4 and wikiHandler not in handler_list:
            handler_list.append(wikiHandler)


        if esHealthHandler not in handler_list:
            handler_list.append(esHealthHandler)
    
        for h in handler_list :
            basic_res = h(self.processmsg,typeWords) 
            #print('handle by'+str(h))
            if basic_res != '':
                return basic_res
         
       # if response == '': # can't find any answer try for BibleHandler
       #     response = esBibleHandler(msg, words)

          
        if response == '': # can't find any answer give 20% for pttHandler
            if random.randint(0,7) < 1:
                response = pttHandler(msg, nounWords)

        if response == '' and not toCommand and len(nounWords)>0 and random.randint(0,5) < 3 :
            careonly = self.randomAct('careonly_res')
            careString = ''
            cnt = 1
            for n in nounWords:
                if cnt > 1:
                    careString = careString + " "+n
                else:
                    careString = careString + n
                cnt+=1
            response = careonly.format(careString)

        if response == '' and toCommand :
            cannotDo = self.randomAct('list_cannot_do')
            showN = ''
            for n in nounWords:
                showN = showN + n
            if toCmdAct != '' and showN != '':
                response = cannotDo.format(toCmdAct, showN)

        if response == '':
            #TODO put in will do list
            willDoList = self.kb['will_do'].split(";")
            for wd in willDoList:
                if msg.count(wd):
                    response = self.randomAct('will_do_res')
                    return response
                    break
           
#        if response == '' and len(self.processmsg) > 5: # can't still can't find any answer 
#            response = esHealthHandler(msg, words, mscore=0.77)

        if response == '':
            #print(self.notFoundResList)
            if len(self.notFoundResList) > 0:
                response = random.choice(self.notFoundResList)
            else: 
                response = random.choice(self.kb['act_no_info'].split(';'))

        return response.strip()





fbBrain = SocialBrain()
gBrain = GenericBrain('happyrun','q')
#genBrain = GenericEnBrain()
if __name__ == '__main__' :

    msg = sys.argv[1]

    from twMessageProcess import  getIntent
    intent = getIntent(msg)
#    print(gBrain.think(intent))
    r = fbBrain.think(intent)
    print("social brain result")
    print(r)



