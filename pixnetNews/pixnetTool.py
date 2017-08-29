
import re
import random
import requests
import sys
import datetime
import json

from nocheckin import client_id
API_URL = 'https://emma.pixnet.cc/mainpage/blog/categories/hot_weekly/30?per_page=12&format=json&client_id='+client_id
FANS_API_URL = 'https://emma.pixnet.cc/mainpage/blog/categories/hot_weekly/30?per_page=21&format=json&client_id=084e1fa57f6e8d1d9700499656e02b7c&client_id='+client_id
FOOD_API_URL = 'https://emma.pixnet.cc/mainpage/blog/categories/hot_weekly/26?per_page={}&format=json&page={}&client_id='+client_id
ARTICLE_URL = 'https://emma.pixnet.cc/blog/articles/{}?user={}&format=json&client_d='+client_id
HOTNEWS_API_URL = 'https://emma.pixnet.cc/mainpage/blog/categories/hot_weekly/{}?per_page={}&format=json&page={}&client_id='+client_id


def analysisArticle(userName, articleNo):
    r = requests.get(ARTICLE_URL.format(articleNo, userName))
    bodyHtml = json.loads(r.text)['article']['body']
    adCount = bodyHtml.count('<ins class') +0.001
    picCount = bodyHtml.count('<img')
    alertMsg = ''
    #print(adCount)
    #print(picCount)
    if adCount >= 2:
        alertMsg = '不過 這篇廣告超級多!!'
#    p = re.compile(r'<.*?>')
#    result = p.sub('',bodyHtml)
#    for line in result.split("\n"):
#        line = line.strip()
#        if '延伸閱讀' in line : 
#            break
#        if line == '' or line =='(adsbygoogle = window.adsbygoogle || []).push({});' or line == '&nbsp;': 
#            continue 
#        
#    bodyHtml = re.sub(r'\&lt;.*?\&gt;', '', bodyHtml)
    return alertMsg

def getHotNews(cata, keyword, maxPageCnt, articlesPerPage):
    newsList = []
    cntPage = maxPageCnt
    cnt = 1 
    while(cnt <= cntPage):
        url =  HOTNEWS_API_URL.format(cata, articlesPerPage,cnt)
        r = requests.get(url)
        #print(cnt)
        cnt += 1
        a = json.loads(r.text)
        #print("---")
        #print(a)
        if 'articles' not in a:
            break
        for article in a['articles']:
            total = article['hits']['total']
            daily = article['hits']['daily']
            if total <= 319: # magic number to identify hot article
                continue
            if keyword in article['title']:
                newsList.append(article)
                continue
            else:
                for t in article['tags']:
                    if keyword == t['tag']:
                        newsList.append(article)
                        #print('got the tag')
                        continue
                continue

        if len(newsList) >= 3: # if got least 3 
            #print(newsList)
            break

    #print(len(newsList))
    return newsList

def getTravelNews(keywords, kuso=True):
    newsList = []
    for keyword in keywords:
        newsList = getHotNews(29,keyword,8,25)
        if len(newsList) <= 0:
            newsList = getHotNews(28,keyword,8,25)
        if len(newsList) > 2:
            break

    if len(newsList) <= 0:
        return ("歹勢 最近沒在{}的新消息".format(keyword) , {})

    #print(len(newsList))
    n = random.choice(newsList)
    title = n['title']
    link = n['link'].split('-')[0]
    writer = n['user']['display_name']
    msg = '最近"{}" 寫了旅記"{}" 可以參考唷~ \n{}'.format(writer, title, link)
    if kuso == True:
        kusoMsg = ''
        anaResult = analysisArticle(n['user']['name'], n['id'])
        if anaResult != '':
            msg = msg + "\n" + anaResult
        else:
            print('no special')

    return msg


 
def getFoodNews(location='', kuso=False):
    newsList = []
    msg = ''
    cntPage = 8

    cnt = 1 
    while(cnt <= cntPage):
        r = requests.get(FOOD_API_URL.format(33,cnt))
        #print(cnt)
        cnt += 1
        a = json.loads(r.text)
        #print(a)
        for article in a['articles']:
            total = article['hits']['total']
            daily = article['hits']['daily']
            if location != '':
                if 'address' not in article:
                    continue
                elif location not in article['address']:
                    continue
                else: 
                    pass
            if total <= 319: # magic number to identify hot article
                continue
            if 'location' not in article:
                continue
            newsList.append(article)

        if len(newsList) >= 7:
            break

    if len(newsList) <= 0:
        return ("歹勢 最近沒在{}的新美食文".format(location) , {})

    n = random.choice(newsList)
    title = n['title']
    link = n['link'].split('-')[0]
    address =n['address']
    writer = n['user']['display_name']
    longitude = n['location']['longitude']
    latitude = n['location']['latitude']
    geo = {'longitude': longitude, 'latitude': latitude, 'address': address}
    msg = '最近"{}" 寫了美食文："{}" 可以考慮去試看看唷~ \n地點:{} \n{}'.format(writer, title, address, link)
    if kuso == True:
        kusoMsg = ''
        anaResult = analysisArticle(n['user']['name'], n['id'])
        if anaResult != '':
            msg = msg + "\n" + anaResult

    return (msg, geo)

def getFansNews():
    r = requests.get(FANS_API_URL)
    a = json.loads(r.text)
    newsList = []
    msg = ''
    for article in a['articles']:
        total = article['hits']['total']
        daily = article['hits']['daily']
        if total <= 319:
            continue
        if "(H)" in article['title']:
            continue

        newsList.append(article)

    if len(newsList) == 0:
        msg = '老實說最近偶像明星還真沒什麼特別的事情...'
        return msg

    oneNews = random.choice(newsList)
    
    link = oneNews['link'].split('-')[0]
    #print("catagory "+ article['category'])
    #print("site catagory "+ article['site_category'])
    title = oneNews['title']
    writer = oneNews['user']['display_name']
    msg = "一些偶像明星消息：{}, \n 請看這裡: {} \n 資料來源: {}".format(title, link, writer)
    return msg


if __name__ == '__main__':
 #   print(getFansNews())
    
#    print(getFoodNews(location = sys.argv[1] , kuso=True))
    print(getTravelNews( [ sys.argv[1] ]))
