
import re
import random
import requests
import sys
import datetime
import json

API_URL = 'https://emma.pixnet.cc/mainpage/blog/categories/hot_weekly/30?per_page=12&format=json'
FANS_API_URL = 'https://emma.pixnet.cc/mainpage/blog/categories/hot_weekly/30?per_page=21&format=json'
FOOD_API_URL = 'https://emma.pixnet.cc/mainpage/blog/categories/hot_weekly/26?per_page=21&format=json'


def getFoodNews():
    r = requests.get(FOOD_API_URL)
    a = json.loads(r.text)
    newsList = []
    msg = ''
    for article in a['articles']:
        total = article['hits']['total']
        daily = article['hits']['daily']
        if total <= 400:
            continue
        if "(H)" in article['title']:
            continue
        if 'location' not in article:
            continue
        newsList.append(article)

    n = random.choice(newsList)
    title = n['title']
    link = n['link'].split('-')[0]
    address =n['address']
    writer = n['user']['display_name']
    longitude = n['location']['longitude']
    latitude = n['location']['latitude']
    geo = {'longitude': longitude, 'latitude': latitude, 'address': address}
    msg = '最近{} 寫了美食文：{} 可以考慮去試看看唷 \n地點:{} \n{}'.format(writer, title, address, link)
    return (msg, geo)

def getFansNews():
    r = requests.get(FANS_API_URL)
    a = json.loads(r.text)
    newsList = []
    msg = ''
    for article in a['articles']:
        total = article['hits']['total']
        daily = article['hits']['daily']
        if total <= 400:
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
    print(getFansNews())
    print(getFoodNews())
  

