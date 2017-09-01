#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# for quick and dirty config.
MatchGFMsg = {
    'lambda' : 'lambda_kbhandler',
    'params' : {'msg':u'如何交到女朋友' , 'index':'testi', "field":'pkey',"res":"res", "score":2.2  },
    'resTemplate' : ['{}',
                     '小姍查了一下知識庫 覺得...{}',],
    'criteries': [
                   [('intent','有'), ('entity','怎樣'),('entity','女朋友')],
                   [('intent','交到'), ('entity','如何'),('entity','女朋友')],
                   [('intent','交到'), ('entity','怎樣才能'),('entity','女朋友')],
                   [('intent','交到'), ('entity','才能'),('entity','女朋友')],
                   [('entity','如何'),('entity','追女生')],
                 ]
}
MatchBeHappyMsg = {
    'lambda' : 'lambda_kbhandler',
    'params' : {'msg':u'快樂的方法' , 'index':'testi', "field":'pkey',"res":"res", "score":2.1  },
    'resTemplate' : ['我一直都會陪你聊天 或者你也可以試一下：{}',
                     '其實...{}',
                     '有個方法:{}... 總之小姍會陪你聊天你就會高興一些了'],
    'criteries': [
                   [('intent','心情'), ('entity','不'),('entity','快樂')],
                   [('intent','覺得'), ('entity','不快樂')],
                   [('intent','不太好'), ('entity','心情')],
                   [('entity','心情'), ('entity','不好')],
                   [('entity','怎樣'), ('intent','會'),('entity','快樂')],
                 ]
    }

MatchActTravel = {
    'lambda' : 'pixnettravel',
    'criteries':[ [('intent','推薦'),('entity','景點'),('location','')],
                  [('intent','好玩'),('entity','地方')],
                  [('intent','好玩'),('entity','哪裡'),('location','')],
                  [('intent','好玩'),('entity','哪邊'),('location','')],
                  [('intent','推薦'),('entity','觀光'),('entity','景點')],
                ]
    }


# to be replace bu MatchActXXXXX latter. (TODO)
MapActions = [
    { 'call_back': 'actPixnetFans',
      'terms' : [ 
                  u'你有認識什麼偶像明星嗎',
                  u'我想知道偶像明星的小道消息',
                  u'我是個沒救的韓流鐵粉',
                  u'最新的偶像明星消息',
                  u'偶像明星消息',
                ]
    },
    { 'call_back': 'actPixnetFood',
      'terms' : [ 
                  u'請推薦餐廳',
                  u'請推薦美食',
                  u'美食推薦',
                  u'餐廳推薦',
                  u'介紹一下美食',
                  u'推薦附近美食',
                  u'推薦附近餐廳',
                  u'請推薦附近美食',
                  u'隨便推薦好吃的',
                  u'隨便推薦好吃的',
                  u'好吃的餐廳',
                  u'有什麼好吃的',
                  u'推薦吃什麼好',
                  u'要吃什麼啊',
                  u'晚上要吃什麼啊',
                ]
    },
    { 'call_back': 'actEventReg',
      'terms' :
                   [u'請通知我天氣特報' ,
                     u'請通知激烈天氣特報',
                     u'停止通知我天氣特報',
                     u'停止通知天氣特報',
                     u'不要通知我天氣特報',
                     u'不要通知天氣特報',
                     u'小姍請通知我天氣特報',
                     u'小姍通知我激烈天氣特報',
                     u'通知激烈天氣特報',
                     u'請每天教我一句英文',
                     u'請給我每日一句學英文',
                     u'小姍請給我每日一句學英文',
                     u'小姍給我每日一句學英文',
                     u'每日一句學英文',
                     u'自動給我每日一句學英文',
                     u'通知天氣特報', 
                     u'請通知最近謠言破解',
                     u'請通知我最近謠言破解',
                     u'請協助我破解網路謠言',
                     u'請幫我破解網路謠言',
                     u'請協助我謠言破解',
                     ]
        },
        {'call_back': 'actWishes',
         'terms': [u'我想許願']
         },
        {'call_back': 'actTaipeiBus',
         'terms': [u'幫我查公車', u'請幫我查公車', u'小姍幫我查公車', u'公車在哪裡', u'請幫我查公車']
         },
        {'call_back': 'actLottery',
         'terms': [u'幫我抽根籤', u'請幫我抽個籤', u'小姍幫我抽簽', u'幫我抽簽看看', u'再幫我抽一次', u'請幫我抽支籤', u'請幫大姐抽支籤', u'請幫我抽籤']
         },
        {'call_back': 'actAstro',
         'terms': [u'今天星座運勢', u'跟我說今天星座運勢', u'小姍幫我查星座運勢', u'幫我看星座運勢', u'幫我查今日星座運勢', u'今日星座運勢',u'小姍幫我查今日星座']
         },
        {'call_back': 'actDayfortune',
         'terms': [u'幫我算命 ', u'出生運勢', u'小姍幫我查出生運勢', u'幫我看出生運勢', u'請幫我算命 生日是', u'請幫我算命',u'幫我算命生日是',u'請幫我算命生日是']
         }
]
