#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jieba
import jieba.posseg as pseg
import argparse

jieba.load_userdict('data/dict.txt.big')

matchActTravel = { 
    'lambda' : 'pixnettravel',
    'criteries':[ [('intent','推薦'),('entity','景點'),('location','')],
                  [('intent','好玩'),('entity','地方')],
                  [('intent','推薦'),('entity','觀光'),('entity','景點')],
                ] 
    }

def getIntent(msg):
    msg = msg.strip()
    tWord = ''
    verb = ''
    entity = []
    timing = []
    location = ''
    oriMsg = msg
 
    if len(msg) <= 5 :
        entity.append(msg)

    words = pseg.cut(msg)

    pnv = False
    pflag = ''
    tmpN = ''
    for word in words:
        if word.flag in  ['nz','nt','n']:
            tmpN = tmpN + word.word
            entity.append(tmpN)
            entity.append(word.word)
            pnv = True
            tmpN = word.word
        elif word.flag in  ['v','vi','vn','vr']:
            verb = word.word
        elif word.flag in  ['r','nr','l','d','a']:
            entity.append(word.word)
        elif word.flag in ['t','tg']:
            timing.append(word.word)
        elif word.flag in ['f','ns']:
            if pflag in ['f','ns']:
                location = location + word.word
            else:
                location =  word.word
    
        else:
            tmpN = ''
            pnv = False
        pflag = word.flag

    intent = { 'intent':verb, 'timings':timing, 'location':location, 'entities': list(set(entity)), 'msg':oriMsg}
    return intent



def decideAction(intent, matchAct):
    for c in matchAct['criteries']:
        toMatch = len(c)
        for (p,v) in c:
            if p == 'intent':
                if intent[p] != v :
                    continue 
            if p == 'entity':
                if v not in intent['entities']:
                    continue 
            if p == 'location':
                if v not in intent[p]:
                    continue 
            toMatch -= 1
        if toMatch <= 0:
            return matchAct
           
    return ""

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='zh_TW Message tool')
    parser.add_argument('--msg','-m', help='specify message string for intent analysis')
    parser.add_argument('--msgFile','-f', help='specify message file for intent analysis')
    
    args = parser.parse_args()
    allIntent = []

    if args.msg is not None: # analysis an intent
        itent = getIntent(args.msg.strip())
        print(itent)
        print(decideAction(itent, matchActTravel))
        exit(0)

    if args.msgFile is not None:
        with open(args.msgFile, 'r') as  infile:
            for line in infile:
                itent =getIntent(line.strip())
                if itent['intent'] != '':
                    allIntent.append(itent['intent'])
    
        with open("verbs",'w') as outfile:
            for i in allIntent: 
                outfile.write(str(i)+"\n")
                outfile.flush() 

        exit(0)

