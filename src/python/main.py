#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import jieba
import jieba.posseg as pseg
from pprint import pprint
from brain import WikiBrain


userReq =":None" 

defaultAction = {'.exit':'離開','.help':'系統說明'}

jieba.set_dictionary('data/dict.txt.big')


wikiBrain = WikiBrain()
def loadBrain():
    with open('default_dialog.json') as data_file:    
        data = json.load(data_file)
 

def think(userSession):
    return wikiBrain.think(userSession)
 
if __name__ == '__main__':

    dialog = loadBrain()
    userSession = {"name":"","lastWords":"", "lastString":""}

    while( userReq.count('.exit') == 0 ):
        userReq = input('Your Message:')
        #words = jieba.cut(userReq, cut_all=False)
        words = pseg.cut(userReq)
        userSession["lastWords"]  = words
        userSession["lastString"]  = userReq
        print("...")
        print(think(userSession))
        print("---")
        
