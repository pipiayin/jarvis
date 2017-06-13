#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests

class Brain():
    def think(self, userSession):
        pass

class WikiBrain(Brain):
   
    maxN = ''
    maxX = ''

    wikiAPI = u'https://zh.wikipedia.org/w/api.php?uselang=zh_tw&action=query&prop=extracts&format=xml&exintro=&titles='

    def load(self, info):
        print("load information")  
   
    def think(self, userSession):
        word_n = {}
        word_x = {}
        result = u'不懂你的意思'
        for word in userSession["lastWords"]:
            # print(word)
            if word.flag == 'n' or word.flag =='x':
                wikiResult = self.findWiki(word)
                if wikiResult == '':
                    return result
                else:
                    return wikiResult
            else:
                pass
        return result
        

    def findWiki(self, word):
        # print(word)
        r  = requests.get( self.wikiAPI+word.word )
        # print(r.encoding)
        #print(dir(r))
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




