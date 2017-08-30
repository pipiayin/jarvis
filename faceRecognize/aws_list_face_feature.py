#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from __future__ import print_function 
import json
import sys
import boto3
import json
import time
import random
import boto3
import requests
from nocheckin import XLineToken
from compare_landmark import compareLandMark


def listBeauty(bucket):
    rclient = boto3.client('rekognition')
    s3 = boto3.resource('s3')
    sbucket = s3.Bucket(bucket)

    bc = 2
    allBeautyFace = {}
    for o in sbucket.objects.all():
        response = rclient.detect_faces(
            Image={
                'S3Object': {
                'Bucket': bucket,
                'Name': o.key
                 }
            },
            Attributes=[ 'ALL' ]
        )

        allBeautyFace[o.key] = response['FaceDetails']


    jstring = json.dumps(allBeautyFace)
    f = open('allBeautyJson',"w")
    f.write(jstring)
    f.flush()
    f.close()


if __name__ == '__main__':
    import sys
    from exampleLM import landmarkS2,landmark1
    #bucket = sys.argv[1]
    #listBeauty(bucket)
    beautyList = {} 
    with open('allBeautyJson') as data_file:    
        beautyList = json.load(data_file)

    for k in beautyList:
        print('---- '+ k+" to stanger")
        print(compareLandMark(landmark1, beautyList[k][0]['Landmarks']))
