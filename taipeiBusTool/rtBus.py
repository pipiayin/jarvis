#!/usr/bin/python
# -*- coding: utf-8 -*-
# real time bus information
# source
#route -> http://data.taipei/bus/ROUTE
#bus -> http://data.taipei/bus/BUSDATA
import gzip
import requests

def buildRTBuses():
    busdata = requests.get("http://data.taipei/bus/BUSDATA")
#    print(busdata.headers)
    busdata.encoding = 'utf-8'
    zipdata = busdata.content
    data = gzip.decompress(zipdata)
    busDict = eval(data)
    routedara = requests.get("http://data.taipei/bus/ROUTE")
    zipdata = routedara.content
    data = gzip.decompress(zipdata)
    routeDict = eval(data)
    
    return busDict, routeDict 

def getBus(busDict, routeDict, nameZh):

    rlist = []
    blist = []
    for k in routeDict['BusInfo']:
        if k['nameZh'] == nameZh :
            rlist.append(k['pathAttributeId'])

    rSet = set(rlist)
    for b in busDict['BusInfo']:
        if int(b['RouteID']) in rSet:
            blist.append(b)
    
    return blist


#def showBus(busNo):
#    print(busNo)
    

if __name__ == '__main__' :
    #try 藍15
    busDict, routeDict = buildRTBuses()
    blist = getBus(busDict, routeDict, u'236')
    
