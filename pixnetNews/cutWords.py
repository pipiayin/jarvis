
#to build knowledge from pixnet datasets
import json
import sys

import re
def striphtml(data):
    p = re.compile(r'<.*?>')
    text = p.sub('', data)
    text = text.replace("\n","").replace("&nbsp;","")
    return text

if __name__ == '__main__':
    if len(sys.argv) <3 :
        print("usage: python3 "+sys.argv[0]+" <input file name> <output file name>")
        exit(0)

    f = sys.argv[1]
    of = sys.argv[2]

    cnt = 0
    with open(f,'r') as inputFile, open(of, 'w') as outFile:
        for line in inputFile:
            cnt += 1
            print(cnt)
            oneDict = json.loads(line.strip())
#            print(oneDict.keys())
#            print("---")
            oneLine = striphtml(oneDict['content'])
            outFile.write(oneLine+"\n")
        outFile.flush()
    
