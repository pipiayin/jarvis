#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jieba
import jieba.posseg as pseg
import argparse

jieba.load_userdict('data/dict.txt.big')

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
    tmpN = ''
    for word in words:
        print(word.flag+" "+word.word)
        if word.flag in  ['nz','nt','n']:
            tmpN = tmpN + word.word
            entity.append(tmpN)
            pnv = True
            tmpN = word.word
        elif word.flag in  ['v','vi','vn','vr']:
            verb = word.word
        elif word.flag in  ['r','nr','l']:
            entity.append(word.word)
        elif word.flag in ['t','tg']:
            timing.append(word.word)
        elif word.flag in ['f','ns']:
            location = word.word
        else:
            tmpN = ''
            pnv = False

    intent = { 'intent':verb, 'timings':timing, 'location':location, 'entities': entity, 'msg':oriMsg}
    return intent


matchAct1 = [('intent','是'),('entities','什麼')]
def decideAction(intent, matchAct):
    result = False
    for (p,v) in matchAct:
        if v not in intent[p]:
            return False
    return True

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='zh_TW Message tool')
    parser.add_argument('--msg','-m', help='specify message string for intent analysis')
    parser.add_argument('--msgFile','-f', help='specify message file for intent analysis')
    
    args = parser.parse_args()
    allIntent = []

    if args.msg is not None: # analysis an intent
        itent = getIntent(args.msg.strip())
        print(itent)
        print(decideAction(itent, matchAct1))
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

