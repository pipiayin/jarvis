# -*- coding: utf-8 -*-

from __future__ import print_function 
import json
import boto3
import sys
import datetime
import requests
from nocheckin import XLineToken
from wikiFinder import findWikiCN


lambda_client = boto3.client('lambda')

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
        msg = u'這個相片裡的人都不太有名...'

    if len(response['CelebrityFaces']) > 0 :
        msg = ''
        for f in response['CelebrityFaces']:
            cname = findWikiCN(f['Name'])
            msg = msg +  u'這張相片中的人 似乎和 {} {}有 {}的相似度 '.format(f['Name'],cname, f['MatchConfidence'])
            msg = msg + "\n"
            
            if len(f['Urls']) > 0:
                msg = msg+ " 請參考下列網址:\n"
                for url in f['Urls']:
                    msg = msg + url+"\n"
               
    print(msg)
    return msg

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
        cresponse = recognizeCelebrities(objKeyString)
       
        msg = analysisFaceRec(cresponse)
        
        toLineResponse={'uid':uid, 'msg':msg}
        if msg == '':
            return

        lresponse = lambda_client.invoke(
             FunctionName='lineResponse',
             InvocationType='Event',
             LogType='None',
             ClientContext='string',
             Payload=json.dumps(toLineResponse),
         )

        bossid = u'Uc9b95e58acb9ab8d2948f8ac1ee48fad'
        msg = msg +"\n 有人送圖來-> \n"

        toBossResponse={'uid':bossid, 'msg':msg, 'imageurl':"https://s3-us-west-2.amazonaws.com/sandyiface/"+objKeyString }
        lresponse = lambda_client.invoke(
             FunctionName='lineResponse',
             InvocationType='Event',
             LogType='None',
             ClientContext='string',
             Payload=json.dumps(toBossResponse),
         )

        return 
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
