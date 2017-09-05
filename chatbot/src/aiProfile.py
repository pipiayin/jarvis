
import sys


from aiConfig import AI_PROFILE 

def getMatchFromIntent(intent,profile=AI_PROFILE):

    for k in AI_PROFILE.keys():
        p = AI_PROFILE[k]
        if 'lenRange' in p:
            if len(intent['msg']) not in range(p['lenRange'][0], p['lenRange'][1]):
                continue
        

        for c in p['criteries']:
            toMatch = len(c)
            for (oneC,oneV) in c:
                if oneC == 'intent':
                    if intent[oneC] != oneV :
                        continue
                if oneC == 'entity':
                    if oneV not in intent['entities']:
                        continue
                if oneC == 'location':
                    if oneV not in intent[oneC]:
                        continue
                toMatch -= 1
            if toMatch <= 0:
                return p

    return ""



if __name__ == '__main__' :
    intent = {'intent': '學習', 'timings': [], 'entities': ['你', '怎麼'], 'msg': '你是怎麼學習的', 'location': ''}
    intent = {'entities': ['如何', '聊天機器人'], 'msg': '如何製作聊天機器人', 'timings': [], 'intent': '製作', 'location': ''}
    resp = getMatchFromIntent(intent)
    print(resp)


