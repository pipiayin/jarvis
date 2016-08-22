#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import json
import requests
import jieba
import jieba.posseg as pseg
import random
import time
import sys

class SocialBrain():

    def basicParser(self, msg):
        response = ""
        print(len(msg))
        if len(msg) >= 60:
            response = u'抱歉一次講太多我聽不懂，可以簡潔一點，60個字之內就好?'
            print('what?? too long')
        return response

    def load(self, info):
        print("load information")

    def think(self, userSession):
        response =u'有什麼可以幫您服務的地方？'
        msg = userSession["msg"]  
        basic_res = self.basicParser(msg) 
        if basic_res != '':
            return basic_res
         
        return response




if __name__ == '__main__':

    fbBrain = SocialBrain()
    
    jieba.set_dictionary('data/dict.txt.big')

    msg = sys.argv[1]
    userSession = {"name":"","lastWords":"", "lastString":""}
    userReq = u'照片不錯'
    words = pseg.cut(userReq)
    userSession["lastWords"]  = words
    userSession["msg"]  = msg

    print(fbBrain.think(userSession))



