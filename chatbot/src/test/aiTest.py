#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import json
import requests
import sys

if __name__ == '__main__':

    msg = sys.argv[1]
    s = open('apikey.so')
    apiKey =  s.readline().strip()
    s.close()
    headers = {'Content-Type': 'application/json', 'x-api-key':apiKey}

    url = 'https://csul2m26h5.execute-api.us-east-1.amazonaws.com/prod/ai'
    payload = json.dumps({ "msg" : msg  })
    r = requests.post(url, headers=headers, data = payload)
    resj = json.loads(r.text)
    print(resj['res'])
