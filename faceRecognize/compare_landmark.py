
import statistics
import json

BeautyList = {}
with open('allBeautyJson') as data_file:
    BeautyList = json.load(data_file)


def getLM(landmarkList, typeName):
    for i in landmarkList:
        if i['Type'] == typeName:
            return (i['X'], i['Y'])

def getDistance(base, target):
    distX = base[0] - target[0] 
    distY = base[1] - target[1]
    dist = (distX**2 + distY**2)**0.5
    return dist

def getDistanceFromType(landmarkList, typeName1, typeName2):
    type1 = getLM(landmarkList,typeName1)
    type2 = getLM(landmarkList,typeName2)
    return getDistance(type1, type2)


def compareLandMark(landmarkList1, landmarkList2):
    distList = []
    compareList = [
                   ('eyeRight','nose') ,
                   ('eyeLeft','nose'),
                   ('mouthLeft','nose'),
                   ('mouthRight','nose'),
                   ('mouthUp','mouthDown'),
                   ('mouthLeft','mouthDown'),
                   ('mouthRight','mouthDown'),
                   ('noseRight','eyeRight'),
                   ('leftPupil','rightPupil'),
                   ('nose','rightPupil'),
                   ('leftPupil','nose'),
                   ('noseRight','noseLeft'),
                   ('eyeRight','eyeLeft') ,
                   ('mouthRight','mouthLeft') ,
                   ('mouthRight','eyeRight') ,
                   ('mouthLeft','eyeRight') ,
                   ('mouthRight','eyeLeft') ,
                  ]

    for (m1,m2) in compareList:
        d1 = getDistanceFromType(landmarkList1, m1, m2)
        d2 = getDistanceFromType(landmarkList2, m1, m2)
        distance = (abs(d1-d2)/d1)
        distList.append(distance)


    lenD = len(distList)
    mD = statistics.mean(distList)
    mStd = statistics.stdev(distList)
    #print(mD)
    #print(mStd)
    #print(statistics.stdev(distList))
    mV = statistics.variance(distList)
    conf = (1-mD)**2
    #print('1 - mean) **2')
    #print(conf)
    #print('1-std *(2')
    #print((1-mStd)**2)
    #print('1- var *(2')
    #print((1-mV)**2)

    #print('sum')
    #print(mD * len(distList))
    return conf*100

if __name__ == '__main__':
    from exampleLM import landmark1, landmark2, landmark3
    print('----')
    compareLandMark(landmark1, landmark2)
    print('----')
    compareLandMark(landmark1, landmark3)
