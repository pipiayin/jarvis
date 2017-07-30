
import statistics


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
                   ('eyeRight','eyeLeft') ,
                   ('mouthRight','mouthLeft') ,
                   ('mouthRight','eyeRight') ,
                   ('mouthRight','eyeLeft') ,
                  ]

    for (m1,m2) in compareList:
        d1 = getDistanceFromType(landmarkList1, m1, m2)
        d2 = getDistanceFromType(landmarkList2, m1, m2)
        distance = abs(d1-d2)
        distList.append(distance)


    print(statistics.mean(distList))
    print(statistics.stdev(distList))
    print(statistics.variance(distList))
    return "result"

print('---')
compareLandMark(landmark1, landmark2)
print('---')
compareLandMark(landmark1, landmark3)
