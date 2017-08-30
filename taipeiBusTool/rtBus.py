#!/usr/bin/python
# -*- coding: utf-8 -*-
# real time bus information
# source
#route -> http://data.taipei/bus/ROUTE
#bus -> http://data.taipei/bus/BUSDATA
import gzip
<<<<<<< HEAD
import requests
=======
import gzip
import requests
import json
>>>>>>> b5a1599dc4edb8dd7e3b2d7f95231de91fce0070

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

<<<<<<< HEAD

#def showBus(busNo):
#    print(busNo)
    
=======
def buildRouteBus(busDict, routeDict):
    mapRouteZh = {}
    for k in routeDict['BusInfo']:
        mapRouteZh[str(k['pathAttributeId'])] = k['nameZh'] 

    for b in busDict['BusInfo']:
        if b['RouteID'] not in mapRouteZh:
#            print(b)
            continue 
        busNameZh = mapRouteZh[b['RouteID']]
#        print(busNameZh)
        b['nameZh'] = busNameZh

#    print(len(busDict['BusInfo']))
    return busDict['BusInfo']

def buildGmapCallBack(blist):
    result = "bus_callback("
    result = result + json.dumps(blist)
    result = result +");"
    return result
>>>>>>> b5a1599dc4edb8dd7e3b2d7f95231de91fce0070

if __name__ == '__main__' :
    #try 藍15
    busDict, routeDict = buildRTBuses()
<<<<<<< HEAD
    blist = getBus(busDict, routeDict, u'236')
=======
    allRouteBus = buildRouteBus(busDict, routeDict)
    print(buildGmapCallBack(allRouteBus))
#    blist = getBus(busDict, routeDict, u'藍27')
#    print(buildGmapMarker(blist))
>>>>>>> b5a1599dc4edb8dd7e3b2d7f95231de91fce0070
    
