# -*- coding: utf-8 -*-

from __future__ import print_function 
import json
import boto3
import sys
import requests
import json
import datetime
from rtBus import buildRTBuses, buildRouteBus, buildGmapCallBack

lambda_client = boto3.client('lambda')

# Lambda event call
#               lresponse = lambda_client.invoke(
#                    FunctionName='ailearn',
#                    InvocationType='Event',
#                    LogType='None',
#                    ClientContext='string',
#                    Payload=json.dumps(toLog),
#                )
#

def lambda_handler(even, context):
    try:
        print("-----get message ---")
        # even format: {"uid": , "busname": , "callback"}
        print(even)
        busDict, routeDict = buildRTBuses()
        allRouteBus = buildRouteBus(busDict, routeDict)
        newalljs = buildGmapCallBack(allRouteBus)
        s3 = boto3.resource('s3')
        busfile = s3.Object('taipeibus', 'all.js')
        lastmodify = busfile.last_modified
        current = datetime.datetime.now(datetime.timezone.utc)
        diffsecond = (current - lastmodify).total_seconds()
        if diffsecond >= 300: # five minutes
            busfile.put(Body=newalljs)
            busfile.Acl().put(ACL='public-read')
            print("rebuild businfo to all.js")
        url = "http://taipeibus.s3-website-us-west-2.amazonaws.com/taipeibus.html?busid="+even['busname']
        surl =  json.loads(goo_shorten_url(url))
        print(surl['id'])
        return 
    except:
        print(even)
        print(sys.exc_info()[0])
        return "something wrong"
   
def goo_shorten_url(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyDd27-tBkhVGvbc9HSUS_gQMjB0KwPCloQ'
    payload = {'longUrl':url}
    headers = {'Content-Type':'application/json'}
    r = requests.post(post_url, data=json.dumps(payload), headers=headers)
    return r.text

if __name__ == '__main__':
    import sys

    busDict, routeDict = buildRTBuses()
    allRouteBus = buildRouteBus(busDict, routeDict)
    newalljs = buildGmapCallBack(allRouteBus)
    s3 = boto3.resource('s3')
    busfile = s3.Object('taipeibus', 'all.js')
    lastmodify = busfile.last_modified
    current = datetime.datetime.now(datetime.timezone.utc)
    diffsecond = (current - lastmodify).total_seconds()
    if diffsecond >= 300: # five minutes
        busfile.put(Body=newalljs)
        busfile.Acl().put(ACL='public-read')
        print("rebuild businfo to all.js")

    url = "http://taipeibus.s3-website-us-west-2.amazonaws.com/taipeibus.html?busid=306"
    print(goo_shorten_url(url))
    # To try from command line
