# -*- coding: utf-8 -*-

from __future__ import print_function 
import json
import boto3
import sys
import json
import datetime
from rtBus import buildRTBuses, buildRouteBus, buildGmapCallBack

lambda_client = boto3.client('lambda')


def lambda_handler(even, context):
    try:
        print("-----get message ---")
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
        return 
    except:
        print(even)
        print(sys.exc_info()[0])
        return "something wrong"
   

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

    # To try from command line
