#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jieba
import jieba.posseg as pseg

jieba.load_userdict('data/dict.txt.big')

def getIntent(msg):
    msg = msg.strip()
    tWord = ''
    verb = ''
    entity = []
    timing = []
    location = ''
 
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
        elif word.flag in  ['r','nr']:
            entity.append(word.word)
        elif word.flag in ['t','tg']:
            timing.append(word.word)
        elif word.flag in ['f','ns']:
            location = word.word
        else:
            tmpN = ''
            pnv = False

    intent = { 'intent':verb, 'timings':timing, 'location':location, 'entities': entity}
    print(intent)
    return intent


if __name__ == '__main__' :
    import sys
    msg = sys.argv[1]
    print('process msg:'+msg)
    getIntent(msg)
    
