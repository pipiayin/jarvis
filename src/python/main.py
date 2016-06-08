#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
from pprint import pprint


userReq =":None" 

defaultAction = {'.exit':'離開','.help':'系統說明'}

def loadDefaultDialog():
    with open('default_dialog.json') as data_file:    
        data = json.load(data_file)
        return data
 
def analysisInput(sentense):
    return sentense
 
if __name__ == '__main__':

    dialog = loadDefaultDialog()
  
    pprint(dialog)

    while( userReq.count('.exit') == 0 ):
        userReq = input('Your Message:')
        userRes = analysisInput(userReq)
        print(userRes)
        
