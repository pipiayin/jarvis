# -*- coding: utf-8 -*-

# Just a tool to find a word from wiki

import json
import requests
import sys
import re


def findWikiCN(word):
    url = u'https://en.wikipedia.org/w/api.php?uselang=en_US&action=query&prop=extracts&format=xml&exintro=&redirects=&titles={0}'
    r  = requests.get(url.format(word) )
    result = filterCN(r.text)
    return result

def filterCN( wikiApiRes):
    if wikiApiRes.count('<extract')==0 :
        return ""
    #result = wikiApiRes.split('<extract')[1].split('</extract>')[0]
    result = wikiApiRes.strip()

    result = re.sub(r'\<.*?\>', '', result)
   # result = re.sub(r'（.*?）', '', result)
   # result = re.sub(r'\(.*?\)', '', result)
   # result = re.sub(r'（.*?）', '', result)
    result = re.sub(r'\&lt;.*?\&gt;', '', result)
    result = re.sub(r'\n', '', result)
    #result = re.sub(r',.*', '', result)
    #result = re.sub(r';.*', '', result)

    m = re.search('Chinese.*; ', result)
    possibleName = ""
    if m is None:
        return possibleName
    if len(m.group(0)) >=10:
        possibleName = m.group(0).replace('Chinese','').replace(" ","")
        possibleName = possibleName[0:5]
        possibleName = possibleName.replace(',','').replace(':','').replace(";",'')
        
    return possibleName
#    return result


if __name__ == '__main__':

    msg = sys.argv[1]

    print(findWikiCN(msg))
    
