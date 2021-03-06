
import sys

from aiConfig import AI_PROFILE 

def getMatchesFromIntent(intent,profile=AI_PROFILE):
    matches = []

    for k in AI_PROFILE.keys():
        p = AI_PROFILE[k]
        if 'lenRange' in p:
            if len(intent['msg']) not in range(p['lenRange'][0], p['lenRange'][1]):
                continue
        
        hasExclude = False
        if 'excludes' in p:
            for e in p['excludes']:
                for (oneC,oneV) in e:
                    if oneC == 'intent':
                        if intent[oneC] == oneV :
                            hasExclude = True
                            break
                    if oneC == 'timings':
                        if  oneV in intent[oneC] :
                            hasExclude = True
                            break
                    if oneC == 'entity':
                        if oneV in intent['entities']:
                            hasExclude = True
                            break
                    if oneC == 'location':
                        if oneV  in intent[oneC]:
                            hasExclude = True
                            break
                if hasExclude == True:
                    break

        if hasExclude == True:
            break

        for c in p['criteries']:
            toMatch = len(c)
            for (oneC,oneV) in c:
                if oneC == 'intent':
                    if intent[oneC] != oneV :
                        continue
                if oneC == 'timings':
                    if  oneV not in intent[oneC] :
                        continue
                if oneC == 'entity':
                    if oneV not in intent['entities']:
                        continue
                if oneC == 'location':
                    if oneV not in intent[oneC]:
                        continue
                toMatch -= 1
            if toMatch <= 0:
                matches.append(p)
                continue

    return matches



if __name__ == '__main__' :
    intent = {'intent': '學習', 'timings': [], 'entities': ['你', '怎麼'], 'msg': '你是怎麼學習的', 'location': ''}
    intent = {'entities': ['如何', '聊天機器人'], 'msg': '如何製作聊天機器人', 'timings': [], 'intent': '製作', 'location': ''}
    intent = {'timings': ['生日'], 'oriCut': [('r', '你'), ('uj', '的'), ('t', '生日')], 'intent': '', 'msg': '你的生日', 'entities': ['你的生日', '你'], 'location': ''}
    intent = {'oriCut': [('r', '你'), ('d', '不'), ('v', '喜歡'), ('n', '做什麼')], 'intent': '喜歡', 'entities': ['做什麼', '你', '不'], 'timings': [], 'location': '', 'msg': '你不喜歡做什麼'}
#    intent = {'msg': '今天天氣很不錯唷 你覺得啦', 'intent': '覺得', 'oriCut': [('i', '今天天氣'), ('zg', '很'), ('a', '不錯'), ('x', '唷'), ('x', ' '), ('r', '你'), ('v', '覺得'), ('y', '啦')], 'timings': [], 'entities': ['你', '不錯'], 'location': ''}

    resp = getMatchesFromIntent(intent)
    print(resp)
    import random
    if len(resp) > 0:
        res = random.choice(random.choice(resp)['res'])
        print(res)


