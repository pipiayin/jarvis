#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import sys
import boto3
import csv
import json
import random


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table_match = dynamodb.Table('kbmatch')
table_similar = dynamodb.Table('similar')
#response = table.put_item(
#    Item={'pkey':u'測試一下', u'res':[u'想測試一下而已嗎',u'只是測試而已？'] })
#print(response)
def inSimilar(msg):
    #print(msg)
    try:
        response = table_similar.get_item(
            Key={
                'pkey': msg,
            }
        )
    except:
        #print(e.response['Error']['Message'])
        e = sys.exc_info()[0]
        return str(e)
    else:
        #print("Get Similar succeeded:")
        if 'Item' in response:
            ori = response['Item']['ori']
            print(ori)
            return ori
    return ""
    
def matchHandler(msg, words):
    bindList = []
    lenofwords = len(words)
    for i in range(lenofwords):

        for k in range(lenofwords+1):
            bindstr = "".join(words[i:k])
            if bindstr == '' or len(bindstr) < 3:
                continue 
            bindList.append(bindstr.strip())

    result =""
    msg = msg.strip()
    ori = ""
    ori = inSimilar(msg) # direct match
    if ori == '':
        for w in bindList:
            ori = inSimilar(w)
            if ori != '' :
                break

    if ori == '':
        return result

    #print("to match"+ori)

    try:
        response = table_match.get_item(
           Key={
            'pkey': ori
           }
        )
    except:
        #print(e.response['Error']['Message'])
        return ''
    else:
        #print("Get Match succeeded:")
        if 'Item' in response:
            suglist = response['Item']['res']
            result = random.choice(suglist)

    return result

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("usage: python "+sys.argv[0]+" <keyword> ")
        print("")
        exit(0)

    print(matchHandler(sys.argv[1],[]))


