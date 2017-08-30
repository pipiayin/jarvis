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

def beautyCompare(imageId):
    rclient = boto3.client('rekognition')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('sandyifamousface')
    firstFaceV = 0
    secondFaceV = 0
    firstName = ''
    secondName = ''
    for o in bucket.objects.all():
        #print(o.key)

        response = rclient.compare_faces(
            SourceImage={
                'S3Object': {
                'Bucket': 'sandyiface',
                'Name': imageId,
            }
        },
            TargetImage={
                'S3Object': {
                'Bucket': 'sandyifamousface',
                'Name': o.key,
            }
        },
            SimilarityThreshold = 45 
        )
    
        if len(response['FaceMatches'] ) > 0:
            simV = response['FaceMatches'][0]['Similarity']
            print(o.key+" "+str(simV))
            if simV >  firstFaceV :
                firstFaceV = simV 
                firstName = o.key
            elif simV >= secondFaceV:
                secondFaceV = simV
                secondName = o.key
            else:
                pass         
        if firstFaceV >= 93 :
            break
        if secondFaceV >= 60 and secondName[0:-5] != firstName[0:-5]:
            break
   
    if firstName == '':
        print("no match")
        return {}
    result = {firstName:firstFaceV, secondName:secondFaceV}
    print(result)
    return result

def faceReport(faceDetailDict):
    
    explains = '這是個{} 年齡大概是{}'
    AgeRange = random.randint(faceDetailDict['AgeRange']['Low'],faceDetailDict['AgeRange']['High']-3)
    genderZHDict = {'MALE':'男的','FEMALE':'女的'}
    genderZH = genderZHDict[faceDetailDict['Gender']['Value'].upper()]
    explains = explains.format(genderZH, AgeRange)
    firstEV = 0
    secondEV = 0
    firstE = ''
    secondE = ''
    emotionZHDict = {
        'HAPPY':'快樂的',
        'SAD':'傷心的',
        'ANGRY':'在生氣',
        'CONFUSED':'恍神恍神',
        'DISGUSTED':'不太舒服',
        'SURPRISED':'驚訝',
        'CALM':'頗為鎮定',
    }   
    print(faceDetailDict['Emotions'])
    for e in faceDetailDict['Emotions']:
        if e['Confidence'] > firstEV:
            firstE = e['Type']
            firstEV = e['Confidence']
        elif e['Confidence'] > secondEV:
            secondE = e['Type']
            secondEV = e['Confidence']
        else:
            pass 
    emotionExplain = '\n照片中他看起來是'+ emotionZHDict[firstE.upper()]
    if secondEV > 30:
        emotionExplain = emotionExplain +" 但是有帶有一點點" + emotionZHDict[secondE.upper()]

    return(explains+ emotionExplain)
if __name__ == '__main__':
    import sys
    # headers = {"Content-type": "application/json; charset=utf-8","X-Line-ChannelID" : "1479704687" , "X-Line-ChannelSecret" : "f5e527151c0c039c2f1f41eeb74d3fb0" , "X-Line-Trusted-User-With-ACL" : "ue7f007a54c9cdc5dcd8b0dad74b4e7ad"}
    headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}


    image_id = '6433940320137'
    image_id = '6438421593368'
    image_id = '6436738029032'
    image_id = '6435122147042'
    image_id = '6435122147042'
    image_id = '6438421593368'
    image_id = '6439491741308' #girl
    image_url = 'https://api.line.me/v2/bot/message/{}/content'.format(image_id)
    r = requests.get(image_url, headers=headers, stream=True)
    print(dir(r))

    bArray = None
    with r.raw as data:
        f = data.read() 
        bArray = bytearray(f)

    rclient = boto3.client('rekognition')
    response = rclient.detect_faces(
        Image={
            'Bytes': bArray
        },
        Attributes=[
        'ALL',
       ]
    )
    for key in response:
        print(key)

    
    print(len(response['FaceDetails']))
    for fd in response['FaceDetails']:
        print(faceReport(fd))


