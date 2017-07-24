# -*- coding: utf-8 -*-

from __future__ import print_function 
import json
import boto3
import sys
import datetime
import requests
import random
from nocheckin import XLineToken

from lineTools import getUserDisplayName
from wikiFinder import findWikiCN


lambda_client = boto3.client('lambda')


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
    #print(faceDetailDict['Emotions'])
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

    if faceDetailDict['Sunglasses']['Value']:
        emotionExplain = emotionExplain + "\n不過帶太陽眼鏡的話 我的分析就可能不準確"

    return(explains+ emotionExplain)



def detectFaces(imageId,bucket='sandyiface'):
    rclient = boto3.client('rekognition')

    response = rclient.detect_faces(
        Image={
            'S3Object': {
            'Bucket': 'sandyiface',
            'Name': imageId
             }
        },
        Attributes=[
        'ALL',
       ]
    )

    return response['FaceDetails']



def uploadLineImageToS3(uid, imageId, bucket='sandyiface'):
    headers = {"Content-type": "application/json; charset=utf-8","Authorization" : "Bearer "+XLineToken}

    imageUrl = 'https://api.line.me/v2/bot/message/{}/content'.format(imageId)
    r = requests.get(imageUrl, headers=headers, stream=True)
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    objkey = uid + "_" + imageId+".jpg"
    obj = bucket.Object(objkey)
    with r.raw as data:
        obj.upload_fileobj(data)

    obj.Acl().put(ACL='public-read') 

    return objkey

def recognizeCelebrities(objkey,bucket='sandyiface'):

    rclient = boto3.client('rekognition')
    response = rclient.recognize_celebrities(
    Image = {
            'S3Object': {
            'Bucket': bucket,
            'Name': objkey }
           }
    )
    return response
    


def analysisFaceRec(response):
    #TODO improve message
    msg = ""
    if len(response['CelebrityFaces']) == 0:
        msg = u'這個相片裡的人好像不是名人...'

    if len(response['CelebrityFaces']) > 0 :
        msg = ''
        for f in response['CelebrityFaces']:
            cname = findWikiCN(f['Name'])
            msg = msg +  u'這張相片中的人和 {} {}有 {}的相似度 '.format(f['Name'],cname, f['MatchConfidence'])
            msg = msg + "\n"
            
            if len(f['Urls']) > 0:
                msg = msg+ " 請參考下列網址:\n"
                for url in f['Urls']:
                    msg = msg + url+"\n"
               
    print(msg)
    return msg


def lineResponse(toLineResponse):
    lresponse = lambda_client.invoke(
         FunctionName='lineResponse',
         InvocationType='Event',
         LogType='None',
         ClientContext='string',
         Payload=json.dumps(toLineResponse),
    )

def lambda_handler(even, context):
    #try:
        print("-----In faceRecognize---")
        # even format: {"uid": "botid": , "callback":"lineResponse", "imageId":"image_id_from_line"}
        # TODO: ASSUMPTION, all callback assume go for lineResponse
        # TODO: ASSUMPTION, all image store to the same bucket sandyiface, with name uid_imageid
        print(even)
        uid = '' 
        imageId =  ''
        if 'uid' in even :
            uid = even['uid']
        else:
            return 
        if 'imageId' in even :
            imageId = even['imageId']
        else:
            return 

        objKeyString = uploadLineImageToS3(uid, imageId)
        fresponse = detectFaces(objKeyString)
        msg = ''
        if len(fresponse)>=3:
            msg = '拜託不要用團體照為難我，最多就兩個人好嗎'
            toLineResponse = {'uid':uid, 'msg':msg}
            lineResponse(toLineResponse)
            return "too many people"

        if len(fresponse) <= 0:
            msg = '目前小姍只對有人的照片有興趣'
            toLineResponse = {'uid':uid, 'msg':msg}
            lineResponse(toLineResponse)
            return "not human"

        for fd in fresponse:
            msg = msg + faceReport(fd)+ "\n"

        cresponse = recognizeCelebrities(objKeyString)
       
        msg = msg+ analysisFaceRec(cresponse)
        
        toLineResponse={'uid':uid, 'msg':msg}
        if msg == '':
            return "no result"

        toLineResponse = {'uid':uid, 'msg':msg}
        lineResponse(toLineResponse)

        userDisplayName = getUserDisplayName(uid)
        bossid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
        msg = msg +userDisplayName+":送圖來 \n"

        toBossResponse={'uid':bossid, 'msg':msg, 'imageurl':"https://s3-us-west-2.amazonaws.com/sandyiface/"+objKeyString }
        lineResponse(toBossResponse)

        return "ok"
    #except:
    #    print(even)
    #    print(sys.exc_info()[0])
    #    return "something wrong"
   

if __name__ == '__main__':
    print("TODO: simple test script")
    imageId = u'6435122147042'
    imageId = u'6435265574375'
    imageId = u'6435322417921'
    imageId = u'6435271838359'
    userId =  u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
    even = {'uid':userId, 'imageId':imageId}
    lambda_handler(even, None)
