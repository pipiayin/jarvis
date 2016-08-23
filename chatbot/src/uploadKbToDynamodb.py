#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import boto3
import sys
import csv

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table_match = dynamodb.Table('kbmatch')
table_similar = dynamodb.Table('similar')
#response = table.put_item(
#    Item={'pkey':u'測試一下', u'res':[u'想測試一下而已嗎',u'只是測試而已？'] })
#print(response)

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("usage: python "+sys.argv[0]+" <kb csv file> <simular csv file> ")
        print("")
        exit(0)

    print("load kb csv file to dynamodb")

    with open(sys.argv[1]) as csvfile:
        slines = csv.reader(csvfile, delimiter=',', quotechar='"')
        for line in slines:
            oriKey = line[0].strip()
            swords = line[1].strip().split(";")
            res = []
            for w in swords:
                w = w.strip()
                if w == '':
                    continue
                res.append(w)
            item={u'pkey':oriKey, u'res':res}
            # to make sure similar table always has itself
            item_similar={u'pkey':oriKey, u'ori':oriKey} 
            response = table_similar.put_item(Item=item_similar)
            response = table_match.put_item(Item=item)
            print(response)

    print("load similar key word mapping to dynamodb")
    with open(sys.argv[2]) as sfile:
        slines = csv.reader(sfile, delimiter=',', quotechar='"')
        for line in slines:
            oriKey = line[0].strip()
            swords = line[1].strip().split(";")
            for w in swords:
                w = w.strip()
                if w == '':
                    continue
                item={'pkey':w, u'ori':oriKey}

                print(item)
                response = table_similar.put_item(Item=item)
                print(response)
            
  

