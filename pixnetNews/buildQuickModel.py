#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gensim.models import word2vec
import sys

def main(modelFile, msg):

   # To load a model.
    model = word2vec.Word2Vec.load(modelFile)
    print(type(model.wv))
    print(dir(model.wv))
    print(model.wv.most_similar(msg))
    #i = 1
    #for k in model.wv.vocab.keys():
    #    print(i)
    #    print(k)
    #    i += 1
       
    
  


if __name__ == '__main__':
    modelFile = sys.argv[1]
    msg = sys.argv[2]
    main(modelFile, msg)
