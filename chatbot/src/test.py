import sys
import os

def isRepeating(history):
    #history is list, however, element might be list or string

    inputList = []
    if len(history) <= 3 :
        return False

    for h in history[-3:]:
        if type(h) == type(''):
            inputList.append(h)
        if type(h) == type([]):
            inputList.append(h[0])

    if len(set(inputList)) <= 1:
        return True
    return False

def isCopying(history):
    h = history #just lazy typing
    if len(h) <= 2:
        return False
    currentMsg = ''
    if type(h[-1]) == type(''):
        currentMsg = h[-1]
    if type(h[-1]) == type([]):
        currentMsg = h[-1][0]

    preRes = ''
    if type(h[-2]) == type(''):
        preRes = None
    if type(h[-2]) == type([]):
        preRes = h[-2][1]

    if preRes is not None and preRes == currentMsg:
        return True
    else:
        return False


history_m = ['妳好',['妳好','hello我是小姍'],'妳好',['妳好','我是聊天機器人'],['妳好','我是聊天機器人 很高興認識你'], ['妳好','我是聊天機器人'],['妳好','我是聊天機器人'],'妳好']
history_s = []
history_r = ['妳好',['妳好','hello我是小姍'],'妳好',['妳好','我是聊天機器人'],['妳好','我是聊天機器人 很高興認識你'], ['妳好','我是聊天機器人'],['妳好','我是聊天機器人'],['我是聊天機器人','你不會是']]
history_rs = []


print(isRepeating(history_m))
print(isCopying(history_r))
print(isRepeating(history_s))
print(isCopying(history_rs))
