#!/usr/bin/env python
import os
import commands
import sys
import traceback
import httplib2
import json

httpclient = httplib2.Http()
APIID='f3e2c3a8720782b6d4b0c3c177772cfa'
APIURL='http://api.openweathermap.org/data/2.5/weather?'


if __name__ == '__main__':
    params_string = 'q=Taipei,tw&APIID='+APIID
    params_string = 'lon=121.53&lat=25.05&APIID='+APIID
    url = APIURL + params_string
    resp, content = httpclient.request(url,"GET",None)
    print resp
    print content
