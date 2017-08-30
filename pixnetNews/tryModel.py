
#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gensim.models import word2vec
import sys

def main(modelFile):

   # To load a model.
    model = word2vec.Word2Vec.load(modelFile)
    print(type(model.wv))
    print(dir(model.wv))
    
  


if __name__ == '__main__':
    modelFile = sys.argv[1]
    main(modelFile)
