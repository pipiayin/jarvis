from time import mktime
from datetime import datetime

import feedparser
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  cleantext = cleantext.replace('&nbsp;','')
  return cleantext

def getNotify(pastHours):
    current = datetime.utcnow()
    rssList = ['http://www.fda.gov.tw:8080/TC/rssNewsAboutRumor.ashx'
            ,'http://www.coa.gov.tw/open_data.php?format=rss&func=faq']
    #d = feedparser.parse('http://feeds.feedburner.com/blogspot/english?format=xml')
    #d = feedparser.parse('http://www.fda.gov.tw:8080/TC/rssNewsAboutRumor.ashx')
    result = []
    for rss in rssList: 
        d = feedparser.parse(rss)
        timeRange = 60 * 60 * pastHours 
    
        for e in d['entries']:
            #dt = datetime(*e['updated_parsed'][:6])
            dt = datetime(*e['published_parsed'][:6])
            diffseconds = (current - dt).total_seconds()
            if diffseconds <= timeRange :
                print('=====')
                tmp = "---終結謠言!---\n"cleanhtml(e['title']) + " \n"
                tmp = tmp + cleanhtml(e['summary'])
                print(tmp)
                result.append(tmp)

    return result


if __name__ == '__main__' :
    getNotify(48)
