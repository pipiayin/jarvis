#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import json
import requests
import sys

def pttHandler(msg, words):
    url ='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=1&hl=zh_TW&prettyPrint=false&source=gcsc&gss=.com&sig=8bdfc79787aa2b2b1ac464140255872c&cx=partner-pub-6282720366794148:2717804370&q={0}&googlehost=www.google.com&oq={1}&gs_l=partner.12...0.0.2.58798.0.0.0.0.0.0.0.0..0.0.gsnos%2Cn%3D13...0.0jj1..1ac..25.partner..0.0.0.&callback=google.search.Search.apiary7397&nocache=1472000964508'

    url = url.format(msg,msg)
    # print(url)
    #headers = {'Content-Type': 'application/json', 'x-api-key':apiKey}
    try:
        r = requests.get(url,verify=False )
        rstring =r.text
        rstring = rstring.replace('google.search.Search.apiary7397(','').replace(');','').replace('// API callback','')
        #print('-----')
        rjson = json.loads(rstring)
        return (rjson["results"][0]['contentNoFormatting'])

    except:
        return ""

    return ""
if __name__ == '__main__':

    msg = sys.argv[1]

    print(pttHandler(msg,[]))
    
