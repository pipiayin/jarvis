#!/usr/bin/env python3

# what means useful data here?
#   * possible promotion 
#   * change manager

import sys
import csv
import os
from couchbase import Couchbase
from couchbase.views.iterator import View
from couchbase.n1ql import N1QLQuery

import pyspark
from pyspark import SparkContext

from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import GradientBoostedTrees

couchbase_host='10.1.193.189'
couchbase_bucket='persona'

couchbucket = Couchbase.connect(bucket=couchbase_bucket, host=couchbase_host)
        
ManagerCata = []
leaveCata = []

def prepareLeaverList(leavefile):
#all2015rdleaves
#format example: 20150409        [20150409, "Hank Hsu (RD-TW)", "Hank Hsu (RD-TW) 20150409190647.0Z Sr. Engineer"]
    with open(leavefile) as f:
        content = f.readlines()
        for line in content:
            leaver = line.split(",")[1].replace("\"",'').strip()
            if leaveCata.count(leaver) == 0:
                leaveCata.append(leaver)
    
    
#will got error if already created
#couchbucket.n1ql_query('CREATE PRIMARY INDEX ON personanew').execute()
def getFirstIfExist(theDict, theKey):
    if theKey in theDict:
        if len(theDict[theKey]) >= 1:
            return theDict[theKey][0]

    return ""

def buildDataFromCouchbase(limit,offset):
# LabeledPoint(0.0 stay or 1.0 leave, [<totally 3 fields])
# [3 field below]
# 1. manager id, in catagory
# 2. promote or not, 1 = promoted once, 2 = twice...
# 3. when created
#    data = [
#        LabeledPoint(0.0, [0.0,0]),
#        LabeledPoint(0.0, [1.0,0]),
#        LabeledPoint(1.0, [2.0,1]),
#        LabeledPoint(1.0, [3.0,1]) ]

    result = []

    for one in couchbucket.n1ql_query('SELECT * FROM personanew limit '+str(limit)+' offset '+str(offset)+' '):

        for k in one:
            personName = ""
            personTitle = []
            personManager = []
            promote = 0 # "no promote"
            changeManager = 0 #"no change manager"
            aleaver = 0 # not a leaver
            all_ad_date = list(one[k].keys())
            all_ad_date.sort()
            for ad_date in all_ad_date:
                persondate = one[k][ad_date][1]
                personName = getFirstIfExist(persondate,"name")

                tmpManager = getFirstIfExist(persondate,'manager')
                toAppendManager = tmpManager.split(",")[0].split("=")[-1]
#                indManager = ManagerCata.index(toAppendManager)
                personManager.append(toAppendManager)
                personTitle.append(getFirstIfExist(persondate,'title'))
     
            if personName.find('RD-TW') == -1:
                continue 

            if len(set(personTitle)) > 1:
                promote = 1

            if len(set(personManager)) > 1:
                changeManager = 1

            lastManager = list(set(personManager))[-1]
            if ManagerCata.count(lastManager) == 0:
                ManagerCata.append(lastManager)
            if leaveCata.count(personName) > 0:
               aleaver = 1
            tmpResult = [promote, changeManager, ManagerCata.index(lastManager)]
            aLabeledPoint = LabeledPoint(aleaver, tmpResult)
            result.append(aLabeledPoint)
            
        
    print('-----------')
    return result
            #print(personName+","+changeManager+","+promote+","+str(ManagerCata.index(lastManager)) )
        

def getCataDict():
    return {0:2,1:2,2:len(ManagerCata)}

couchbase_host='10.1.192.79'
couchbase_bucket='personanew'

couchbucket = Couchbase.connect(bucket=couchbase_bucket, host=couchbase_host)

# reference http://spark.apache.org/docs/latest/api/python/pyspark.mllib.html#module-pyspark.mllib.tree

pyspark.StorageLevel(True, False, False, False, 1)
sc = SparkContext("local", "ad RD leave predict")


if __name__ == '__main__':
    prepareLeaverList('../var/all2015rdleaves')
    data = []
    l = 500
    for i in range(6):
        data.extend(buildDataFromCouchbase(l, l*i))

    cataDict = getCataDict()

    model = GradientBoostedTrees.trainClassifier(sc.parallelize(data), cataDict, numIterations=10, maxBins=500)
    print(model.numTrees())
    print(model.totalNumNodes())

    print('===== random predict===')
    idxManager = ManagerCata.index('Alex Tseng (RD-TW)')
    print('idx manager = '+str(idxManager))
    print(model.predict([0.0,0.0,idxManager]))
    print(model.predict([0.0,1.0,idxManager]))
    print(model.predict([1.0,0.0,idxManager]))
    print(model.predict([1.0,1.0,idxManager]))
#    rdd = sc.parallelize([[2.0], [0.0]])
#    model.predict(rdd).collect()
