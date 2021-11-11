"""
查找bad cases

"""

import os
from utils.diff import diff

preDir="./correctFile"
textDir="./textFile"
preFile = os.listdir(preDir)
textFile = os.listdir(textDir)

# preList=getList(preFile,"./preFile")
# textList=getList(textFile,"./textFile")

# for a,b in zip(textList,preList):
#      print('pred: {}, gt: {}'.format(b, a))

with open("bad_cases.txt","w",encoding="utf-8") as f:


    for text in textFile:
        f.write(text+"\n")
        pre=text[:-9]+"_restore.txt_onlyChinese.txt"
        preList = []
        textList = []
        with open(os.path.join(preDir, pre), "r", encoding="utf-8") as fw:
            preList = fw.readlines()
        with open(os.path.join(textDir, text), "r", encoding="utf-8") as fw:
            textList = fw.readlines()

        for aline,bline in zip(preList,textList):
            differences = list(diff(aline, bline))
            if len(differences)!=0:
                f.write("pre:{}text:{}".format(aline,bline))
                print("pre:{}text:{}".format(aline,bline))
            for i1, i2, j1, j2, a, b in differences:
                print("{} {}".format(a,b))
                f.write("{} {}\n".format(a,b))