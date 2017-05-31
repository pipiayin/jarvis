
import requests
import sys
from hanziconv import HanziConv
from datetime import datetime

DAY_TELLER_URL = "http://www.53bang.com/shengri/{}.html"

def getDayContext(allText):
    text = allText.split("name_banner")[1].split("<P>")[1].split("</P>")[0]
    text = HanziConv.toTraditional(text)
    text = text.replace(u'齣生',u'出生')
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
  

