#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Brain():
    def think(self, userSession):
        pass

class WikiBrain(Brain):
   
    maxN = ''
    maxX = ''

    wikiAPI = u'https://zh.wikipedia.org/w/api.php?uselang=zh_tw&action=query&prop=extracts&format=xml&exintro=&titles=澳大利亚'

    def load(self, info):
        print("load information")  
   
    def think(self, userSession):
        for word in userSession["lastWords"]:
            print(word)
            print(word.flag)
        
