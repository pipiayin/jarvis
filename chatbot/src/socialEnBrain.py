#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import json
import requests
import re
import random
import time
import sys
import csv
from esKB import esHandler
from genericKB import genericHandler
from esHealth import esHealthHandler
from wikiFinder import findWikiEn
#from io import open
import codecs
#from pttChat import pttHandler
from wikiChat import wikiHandler
import os
os.environ['NLTK_DATA'] = 'nltk_data'

class GenericEnBrain():
    listIdx = [('enbasic1',0.8), ('enbot1',2.0)]
    kb = {}
    notFoundResList = []

    def __init__(self):

        with open('basickb_en.csv') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                if(len(row)>=2):
                    self.kb[row[0].strip()] = row[1].strip()

    def randomAct(self, actKey):
        res_act = self.kb[actKey].split(";")
        return random.choice(res_act)

    def think(self, msg):
        response = ''
        dirtylist = self.kb['dirty_words'].lower().split(";")
        msg = msg.strip()
        for dword in dirtylist:
            dword = dword.strip()
            if dword in msg:
                return self.randomAct('dirty_words_res')
   
        for cnf in self.listIdx:
            response = genericHandler(cnf[0], 'fb', msg, min_score=cnf[1])
            if response != '':
                return response

        if response == '': # Wikifinedr
            from textblob import TextBlob
            b = TextBlob(msg.lower())
            if len(b.noun_phrases) > 0:
                toFindInWiki = b.noun_phrases[0]
                wikiResponse = findWikiEn(toFindInWiki)
                response = wikiResponse[0:300] + "...<search from wiki>"

        if response == '':
            response = self.randomAct('act_no_info')

        return response
    
genBrain = GenericEnBrain()
if __name__ == '__main__':

    msg = sys.argv[1]

    print(genBrain.think(msg))
#    print(gBrain.think(msg))
#    print(fbBrain.think(msg))



