from time import mktime
from datetime import datetime

import feedparser

def getNotify(pastHours):
    current = datetime.utcnow()
    d = feedparser.parse('http://www.cwb.gov.tw/rss/Data/cwb_warning.xml')
    timeRange = 60 * 60 * pastHours 
    result = []
    
    for e in d['entries']:
        #dt = datetime(*e['updated_parsed'][:6])
        dt = datetime(*e['published_parsed'][:6])
        diffseconds = (current - dt).total_seconds()
        if diffseconds <= timeRange :
            result.append(e['summary'])

    return result


if __name__ == '__main__' :
    print('in past 1 hours')
    print(getNotify(1))
    print('in past 3 hours')
    print(getNotify(3))
