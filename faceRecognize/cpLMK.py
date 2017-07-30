
import statistics

    

landmark1 = [
                {
                    "Type": "eyeLeft",
                    "X": 0.31639400124549866,
                    "Y": 0.40475520491600037
                },
                {
                    "Type": "eyeRight",
                    "X": 0.5623876452445984,
                    "Y": 0.4099090099334717
                },
                {
                    "Type": "nose",
                    "X": 0.42055147886276245,
                    "Y": 0.5130525827407837
                },
                {
                    "Type": "mouthLeft",
                    "X": 0.32774683833122253,
                    "Y": 0.5851089358329773
                },
                {
                    "Type": "mouthRight",
                    "X": 0.5463817715644836,
                    "Y": 0.5963027477264404
                },
                {
                    "Type": "leftPupil",
                    "X": 0.31138479709625244,
                    "Y": 0.40389496088027954
                },
                {
                    "Type": "rightPupil",
                    "X": 0.5552188158035278,
                    "Y": 0.40825706720352173
                },
                {
                    "Type": "leftEyeBrowLeft",
                    "X": 0.2174336314201355,
                    "Y": 0.3546331822872162
                },
                {
                    "Type": "leftEyeBrowUp",
                    "X": 0.28756529092788696,
                    "Y": 0.3352157175540924
                },
                {
                    "Type": "leftEyeBrowRight",
                    "X": 0.36250627040863037,
                    "Y": 0.3480885624885559
                },
                {
                    "Type": "rightEyeBrowLeft",
                    "X": 0.5026174187660217,
                    "Y": 0.353542685508728
                },
                {
                    "Type": "rightEyeBrowUp",
                    "X": 0.5814847946166992,
                    "Y": 0.34236037731170654
                },
                {
                    "Type": "rightEyeBrowRight",
                    "X": 0.6563085913658142,
                    "Y": 0.3601713478565216
                },
                {
                    "Type": "leftEyeLeft",
                    "X": 0.2667829096317291,
                    "Y": 0.40456223487854004
                },
                {
                    "Type": "leftEyeRight",
                    "X": 0.36539721488952637,
                    "Y": 0.4113735258579254
                },
                {
                    "Type": "leftEyeUp",
                    "X": 0.3185333013534546,
                    "Y": 0.3896709978580475
                },
                {
                    "Type": "leftEyeDown",
                    "X": 0.31455856561660767,
                    "Y": 0.41662678122520447
                },
                {
                    "Type": "rightEyeLeft",
                    "X": 0.5125986337661743,
                    "Y": 0.41573330760002136
                },
                {
                    "Type": "rightEyeRight",
                    "X": 0.6112786531448364,
                    "Y": 0.4102476239204407
                },
                {
                    "Type": "rightEyeUp",
                    "X": 0.5605530738830566,
                    "Y": 0.39445769786834717
                },
                {
                    "Type": "rightEyeDown",
                    "X": 0.5646713376045227,
                    "Y": 0.42227891087532043
                },
                {
                    "Type": "noseLeft",
                    "X": 0.3881732225418091,
                    "Y": 0.542183518409729
                },
                {
                    "Type": "noseRight",
                    "X": 0.46989041566848755,
                    "Y": 0.5440884232521057
                },
                {
                    "Type": "mouthUp",
                    "X": 0.4277880787849426,
                    "Y": 0.5857807993888855
                },
                {
                    "Type": "mouthDown",
                    "X": 0.42963701486587524,
                    "Y": 0.6238546967506409
                }
            ]


landmark2 = [
                {
                    "Type": "eyeLeft",
                    "X": 0.3974345922470093,
                    "Y": 0.40445491671562195
                },
                {
                    "Type": "eyeRight",
                    "X": 0.623227059841156,
                    "Y": 0.4721389710903168
                },
                {
                    "Type": "nose",
                    "X": 0.4771824777126312,
                    "Y": 0.5442917346954346
                },
                {
                    "Type": "mouthLeft",
                    "X": 0.3150198757648468,
                    "Y": 0.5573635697364807
                },
                {
                    "Type": "mouthRight",
                    "X": 0.533010721206665,
                    "Y": 0.6215696930885315
                },
                {
                    "Type": "leftPupil",
                    "X": 0.401399165391922,
                    "Y": 0.39791932702064514
                },
                {
                    "Type": "rightPupil",
                    "X": 0.6211731433868408,
                    "Y": 0.46863919496536255
                },
                {
                    "Type": "leftEyeBrowLeft",
                    "X": 0.32841193675994873,
                    "Y": 0.3356545567512512
                },
                {
                    "Type": "leftEyeBrowUp",
                    "X": 0.40833780169487,
                    "Y": 0.3401610553264618
                },
                {
                    "Type": "leftEyeBrowRight",
                    "X": 0.4776400029659271,
                    "Y": 0.3733026385307312
                },
                {
                    "Type": "rightEyeBrowLeft",
                    "X": 0.5890330672264099,
                    "Y": 0.41335517168045044
                },
                {
                    "Type": "rightEyeBrowUp",
                    "X": 0.6547112464904785,
                    "Y": 0.41586923599243164
                },
                {
                    "Type": "rightEyeBrowRight",
                    "X": 0.7070286273956299,
                    "Y": 0.44462868571281433
                },
                {
                    "Type": "leftEyeLeft",
                    "X": 0.347542941570282,
                    "Y": 0.3912672698497772
                },
                {
                    "Type": "leftEyeRight",
                    "X": 0.44129690527915955,
                    "Y": 0.4253099262714386
                },
                {
                    "Type": "leftEyeUp",
                    "X": 0.4067497253417969,
                    "Y": 0.39199891686439514
                },
                {
                    "Type": "leftEyeDown",
                    "X": 0.3911340534687042,
                    "Y": 0.4130774140357971
                },
                {
                    "Type": "rightEyeLeft",
                    "X": 0.5719637274742126,
                    "Y": 0.4651549458503723
                },
                {
                    "Type": "rightEyeRight",
                    "X": 0.6687195301055908,
                    "Y": 0.48610037565231323
                },
                {
                    "Type": "rightEyeUp",
                    "X": 0.6293329000473022,
                    "Y": 0.45863059163093567
                },
                {
                    "Type": "rightEyeDown",
                    "X": 0.6200066804885864,
                    "Y": 0.48215875029563904
                },
                {
                    "Type": "noseLeft",
                    "X": 0.40883758664131165,
                    "Y": 0.5484097003936768
                },
                {
                    "Type": "noseRight",
                    "X": 0.49486199021339417,
                    "Y": 0.5741426944732666
                },
                {
                    "Type": "mouthUp",
                    "X": 0.43638983368873596,
                    "Y": 0.590505063533783
                },
                {
                    "Type": "mouthDown",
                    "X": 0.4065535068511963,
                    "Y": 0.6424179077148438
                }
            ]



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
        d1 = getDistanceFromType(landmark1, m1, m2)
        d2 = getDistanceFromType(landmark2, m1, m2)
        distance = abs(d1-d2)
        distList.append(distance)


    print(statistics.mean(distList))
    print(statistics.stdev(distList))
    print(statistics.variance(distList))
    return "result"

compareLandMark(landmark1, landmark2)
