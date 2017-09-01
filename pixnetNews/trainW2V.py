#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gensim.models import word2vec
import sys

def main(infile, modelFile):

    sentences = word2vec.Text8Corpus(infile)
    model = word2vec.Word2Vec(sentences, size=200)

    # Save our model.
    model.save(modelFile)

    # To load a model.
    # model = word2vec.Word2Vec.load("your_model.bin")

if __name__ == "__main__":
    infile = sys.argv[1]
    modelfile = sys.argv[2]
    main(infile,modelfile)
