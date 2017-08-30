from time import mktime
from datetime import datetime

import re
import feedparser

def clean(msg):
    msg = re.sub(r'&#.{4};', '', msg)
    msg = re.sub(r'相關名言.*', '', msg)
    return msg

def getNotify(pastHours):
    current = datetime.utcnow()
    #d = feedparser.parse('http://www.appledaily.com.tw/rss/newcreate/kind/rnews/type/new')
    #d = feedparser.parse('https://www.managertoday.com.tw/rss')
    d = feedparser.parse('http://feeds.feedburner.com/blogspot/english?format=xml')
    timeRange = 60 * 60 * pastHours 
    result = []
    
    for e in d['entries']:
        #dt = datetime(*e['updated_parsed'][:6])
        dt = datetime(*e['published_parsed'][:6])
        diffseconds = (current - dt).total_seconds()
        if diffseconds <= timeRange :
            contentSummary = e['summary']
            contentSummary = clean(contentSummary)
            result.append(contentSummary)

    return result


if __name__ == '__main__' :
    for r in getNotify(24):
        print('--------')
        print(r)
