#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import jieba
from pprint import pprint



userReq =":None" 

defaultAction = {'.exit':'離開','.help':'系統說明'}

jieba.set_dictionary('dict.txt.big')




def loadBrain():
    with open('default_dialog.json') as data_file:    
        data = json.load(data_file)
        return data
 
def think(sentense):
    return sentense
 
if __name__ == '__main__':

    dialog = loadBrain()
    userSession = {"name":"","lastWords":"", "lastString":""}

    while( userReq.count('.exit') == 0 ):
        userReq = input('Your Message:')
        words = jieba.cut(userReq, cut_all=False)
        userSession["lastWords"]  = words
        userSession["lastString"]  = userReq
        userRes = think(userSession)
        print(userRes)
        
