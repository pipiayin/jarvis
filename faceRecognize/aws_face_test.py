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

def detectModeration(bArray):
    rclient = boto3.client('rekognition')
    response = rclient.detect_moderation_labels(
        Image={
            'Bytes': bArray
        },
        MinConfidence = 60
    )
    return response

def explainModeration(mResponse):
    msg = ''
    for mlabel in mResponse['ModerationLabels']:
        if mlabel['Name'] == 'Explicit Nudity' or mlabel['ParentName'] == 'Explicit Nudity' and mlabel['Confidence'] >=80 :
            msg = '\n經過分析 有{}的信心覺得 這照片恐有傷風敗俗嫌疑...\n'.format(int(mlabel['Confidence'])) 
            msg = msg +"\n小姍不分析 也不想看這類照片 sorry"
            break
        
    return msg


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



  #  url = 'https://trialbot-api.line.me/v1/events'
    """
    url = 'https://trialbot-api.line.me/v1/profiles'
    uids = [ "u0a3d105aa9f8c1ab256dffe226c1d99a", "u1ea21aa1908e6f9db4493f338add1f43", "u41b34094d1078bfd7ac91ae9a0fa2d25", "u47ea331dd00d16c830afef34795b634d", "ua112a584bffbd8898c583669931ee23b", "ubc5b714cecbad5657485548f2a6776fa", "ue38104279bcf8edf0534e038fd151006", "ueda8b2682b70f3bd7b93d72ac58a5e33", "uf234561bda4da2dd46e6486636eb607f",'u9c82e1183eeac7c50124d769d343657c']
    for uid in uids :
        params={"mids":uid}
        r = requests.get(url, headers=headers, params = params)
        print(r)
        print(r.text)
    """
    image_id = '6433940320137'
    image_id = '6438421593368'
    image_id = '6436738029032'
    image_id = '6435122147042'
    image_id = '6435122147042'
    image_id = '6438421593368'
    image_id = '6439491741308' #girl
    image_id = '6445361396005' #modo

    image_url = 'https://api.line.me/v2/bot/message/{}/content'.format(image_id)
    r = requests.get(image_url, headers=headers, stream=True)
    bArray = None
    with r.raw as data:
        f = data.read()
        bArray = bytearray(f)
    #with r.raw  as fd:
    #    print(fd.read())

    dResponse = detectModeration(bArray)
    print(dResponse)
    if len(dResponse['ModerationLabels']) > 0:
        modMsg = explainModeration(dResponse)
        if modMsg != '':
            print(modMsg)
"""
    import boto3
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('sandyiface')
    obj = bucket.Object(image_id)

    with r.raw as data:
        obj.upload_fileobj(data)

    rclient = boto3.client('rekognition')

    response = rclient.detect_faces(
        Image={
            'S3Object': {
            'Bucket': 'sandyiface',
            'Name': image_id
             }
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
        if fd['Gender']['Value'].upper() == 'FEMALE':
            r = beautyCompare(image_id)
            print(r)

    response = rclient.recognize_celebrities(
    Image={
        'S3Object': {
            'Bucket': 'sandyiface',
            'Name': image_id
        }
    }
    )
    for k in response:
        print(k)

    if len(response['CelebrityFaces']) > 0 :
        print("match somebody")
        for f in response['CelebrityFaces']:
            print(f['MatchConfidence'])
            print(f['Name'])
            print(f['Urls'])

"""

