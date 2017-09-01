# -*- coding: utf-8 -*-

import sys
import jieba

def main(infile, outfile):

    jieba.set_dictionary('data/dict.txt.big')

    # load stopwords set
    stopwordset = set()
    with open('data/stop_words.txt','r',encoding='utf-8') as sw:
        for line in sw:
            stopwordset.add(line.strip('\n'))

    texts_num = 0
    
    with open(infile,'r') as content, open(outfile,'w') as output :
        for line in content:
            words = jieba.cut(line, cut_all=False)
            for word in words:
                if word not in stopwordset:
                    output.write(word +' ')
            texts_num += 1
            if texts_num % 10000 == 0:
                print("handled "+str(texts_num))
        output.flush()
    
if __name__ == '__main__':
    infile = sys.argv[1]
    outfile = sys.argv[2]
    main(infile,outfile)
