
import json
import requests
from nocheckin import XLineToken, happyrunXLineToken, botannXLineToken, botyunyunXLineToken, botpmXLineToken, botjhcXLineToken

def getBotHeader(botid):
    botMap = {'happyrun': happyrunXLineToken,
              'botann': botannXLineToken,
              'botpm': botpmXLineToken,
              'botjhc': botjhcXLineToken,
              'botyunyun': botyunyunXLineToken}
    if botid in botMap:
        headers = {"Content-type": "application/json; charset=utf-8",
                   "Authorization": "Bearer " + botMap[botid]}
        return headers
    else:
        return ""

def getUserDisplayName(fromuid, botid=''):
    try:
        line_url = 'https://api.line.me/v2/bot/profile/' + fromuid
        headers = {"Content-type": "application/json; charset=utf-8",
                   "Authorization": "Bearer " + XLineToken}

        if botid != '':
            botHeaders = getBotHeader(botid)
            if botHeaders != '':
                headers = botHeaders

        r = requests.get(line_url, headers=headers)
        rjson = json.loads(r.text)
        ruser = rjson['displayName']
        return ruser
    except:
        print('can not get displayName from uid:' + fromuid)
        return ''




if __name__ == '__main__' :
    print(getBotHeader('happyrun'))
    print(getUserDisplayName(u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'))
