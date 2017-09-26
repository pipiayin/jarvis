#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import fnmatch
import sys
import re
from bs4 import BeautifulSoup




# traverse root directory, and list directories as dirs and files as files
def getFileList(path):
    htmllist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            try:
                print(str(root)+"/"+ file)
                if file.endswith('html'):
                    htmllist.append(str(root)+"/"+ file)
            except UnicodeEncodeError:
                print ("error in encoding")


    return htmllist



def striphtml(data):
    p = re.compile(r'<.*?>')
    text = p.sub('', data)
    text = text.replace("\n","").replace("&nbsp;","")
    return text

if __name__ == '__main__':
    if len(sys.argv) <3 :
        print("usage: python3 "+sys.argv[0]+" <web path> <output file name>")
        exit(0)

    webPath = sys.argv[1]
    of = sys.argv[2]

    htmlFileList = getFileList(webPath)

    cnt = 0
    for f in htmlFileList:
        with open(f) as fp, open(of, 'a') as outFile:
            soup = BeautifulSoup(fp)
            for script in soup(["script", "style"]):
                script.decompose()     # rip it out
            #print(soup.body)
            text = soup.get_text()

# break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

            for l in text.splitlines():
                if len(l) <= 5: 
                    continue
                if len(l) >= 15:
                    print(l)
                outFile.write(l+"\n")
                cnt+=1
                if cnt % 1000 == 0:
                    print("handled {} lines".format(str(cnt)))
