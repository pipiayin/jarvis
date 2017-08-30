
import requests
import sys
from hanziconv import HanziConv
from datetime import datetime

DAY_TELLER_URL = "http://www.53bang.com/shengri/{}.html"

def cleanHanziError(text):
    errorMap = { u'齣生':u'出生',
                 u'方麵':u'方面',
                 u'特彆':u'特別',
                 u'傢':u'家',
                 u'波摺':u'波折',
                 u'纔能':u'才能',
                 u'齣外':u'出外',
                 u'睏':u'困',
                 u'死彆':u'死別'
               }
    for k in errorMap:
        text = text.replace(k,errorMap[k])
    return text
def getDayContext(allText):
    text = allText.split("name_banner")[1].split("<P>")[1].split("</P>")[0]
    text = HanziConv.toTraditional(text)
    text = cleanHanziError(text)
    return text

def getTitleContext(allText):
    text = allText.split("name_ctitle")[1].split("<h2>")[1].split("</h2>")[0]
    text = HanziConv.toTraditional(text)
    return text

def getAllContext(birthday):
    getUrl = DAY_TELLER_URL.format(birthday)
    print(getUrl)
    r = requests.get(getUrl)
    return r.text

def tellTheDay(birthday):
    result = ""
    try:
        datetime.strptime(birthday, '%Y%m%d')
        print("ok")
    except ValueError:
        result = "你輸入的似乎不是真的日期 ("+birthday+")"
    if result != "" :
        return result
    allText = getAllContext(birthday)
    text = getDayContext(allText)
    titleText = getTitleContext(allText)
    return (titleText + "\n" + text)


if __name__ == '__main__':
    day = sys.argv[1]
    print(tellTheDay(day))
  

