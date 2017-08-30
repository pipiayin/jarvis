
import re
import requests
import sys
import datetime
from hanziconv import HanziConv

DAY_TELLER_URL = "http://astro.click108.com.tw/daily_{}.php?iAcDay={}&iAstro={} "
ASTRO = {"水瓶":10, "雙魚":11, "牡羊":0, "金牛":1, "雙子":2, "巨蟹":3, "獅子":4, "處女":5, "天秤":6, "天蠍":7, "射手":8, "魔羯":9}


def cleanHtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def getDayContext(allText):
    text = allText.split("TODAY_CONTENT")[1].split("</div>")[0]
    text = text.replace("\">",'').replace("\t"," ").replace(' ','')
    text = cleanHtml(text)
    #text = HanziConv.toTraditional(text)
    today = str(datetime.date.today())
    return today+ "::" + text


def getAllContext(astro):
    noAstro = str(ASTRO[astro])
    today = str(datetime.date.today())
    getUrl = DAY_TELLER_URL.format(noAstro,today,noAstro)
    print(getUrl)
    r = requests.get(getUrl)
    return r.text

def tellTodayDay(birthday):
    allText = getAllContext(day)
    return getDayContext(allText)


if __name__ == '__main__':
    day = sys.argv[1]
    allText = tellTodayDay(day)
    print(allText)
  

