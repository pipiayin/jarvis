
import sys

import csv

AI_PROFILE = {}
with open('aiprofile.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        if(len(row)>=2):
            AI_PROFILE[row[0].strip()] = row[1].strip()


if __name__ == '__main__' :

    for k in AI_PROFILE:
        print(k)

