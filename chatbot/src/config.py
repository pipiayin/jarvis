
# for quick and dirty config.

MapActions = [
    { 'call_back': 'actPixnetFood',
      'terms' : [ 
                  u'請推薦餐廳',
                  u'請推薦美食',
                  u'推薦附近美食',
                  u'推薦附近餐廳',
                  u'有什麼好吃的',
                  u'推薦吃什麼好',
                  u'要吃什麼啊'
                ]
    }
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
