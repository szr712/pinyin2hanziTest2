import os
import re
from tqdm import tqdm

def cer(r: list, h: list):
    """
    Calculation of CER with Levenshtein distance.
    """
    # initialisation
    import numpy
    d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint16)
    d = d.reshape((len(r) + 1, len(h) + 1))
    for i in tqdm(range(len(r) + 1)):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i
    # computation
    for i in tqdm(range(1, len(r) + 1)):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)
    return d[len(r)][len(h)] / float(len(r))

def getList(fileList,dirPath):
    result=[]
    for file in fileList:
        with open(os.path.join(dirPath, file), "r", encoding="utf-8") as fw:
            contents = fw.readlines()
            result=result+contents
    return result

if __name__=="__main__":
    preFile=os.listdir("./preFile")
    textFile=os.listdir("./textFile")

    preList=getList(preFile,"./preFile")
    textList=getList(textFile,"./textFile")

    # for a,b in zip(textList,preList):
    #      print('pred: {}, gt: {}'.format(b, a))

    print('recpinyin2hanzi CER: {:.3f}'.format(cer(textList, preList)))
    # print('recpinyin2hanzi CER: {:.3f}'.format(cer([""], [""])))

    
