"""
多线程计算CER
需比对文字放入preFile文件夹下
原文放入textFile文件夹下
"""
import os
import re
from tqdm import tqdm
import multiprocess
import math
import time

num_process = 128

def sub_process(textList,preList,result,record,lock,id):
    for t,p in zip(textList,preList):
        record.append(t)
        r = [x for x in t]
        h = [x for x in p]
        cer(r,h,result,lock,id)


def cer(r: list, h: list, result,lock,id):
    """
    Calculation of CER with Levenshtein distance.
    """
    # initialisation
    import numpy
    # print("{}:start initialisation".format(id))
    d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint16)
    d = d.reshape((len(r) + 1, len(h) + 1))
    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i
    # computation
    # print("{}:start computation".format(id))
    for i in range(1, len(r) + 1):
        # lock.acquire()
        # print("{}:  {}".format(id,i))
        # lock.release()
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)
    # lock.acquire()       
    result.append((d[len(r)][len(h)],float(len(r))))
    # lock.release()

def listener(record,total,start,lock):
    now=start
    while total-len(record)>100:
        if time.time()-now>5:
            now=time.time()
            # lock.acquire()
            print("{}/{}, {:.2f}%,cost:{:.2f}m,rest:{:.2f}m".format(len(record),total,len(record)/float(total)*100,(now-start)/60,(now-start)/60/(len(record)/float(total))-(now-start)/60))
            # if len(record)==84952:
            #     print(result)
            # lock.release()


def getList(fileList, dirPath):
    result = []
    for file in fileList:
        with open(os.path.join(dirPath, file), "r", encoding="utf-8") as fw:
            contents = fw.readlines()
            result = result+contents
    return result


if __name__ == "__main__":
    preFile = "./preFile"
    textFile = "./textFile"
    lock = multiprocess.Lock()

    # preList=getList(preFile,"./preFile")
    # textList=getList(textFile,"./textFile")

    # for a,b in zip(textList,preList):
    #      print('pred: {}, gt: {}'.format(b, a))

    for pre in os.listdir(preFile):
        text=pre[:-7]+"_text.txt"
        preList = []
        textList = []
        with open(os.path.join(preFile, pre), "r", encoding="utf-8") as fw:
            preList = fw.readlines()
        with open(os.path.join(textFile, text), "r", encoding="utf-8") as fw:
            textList = fw.readlines()

        start =time.time()

        print("preFileName:{}\ntextFileName:{}".format(pre,text))
        with multiprocess.Manager() as m:
            result = m.list()
            record = m.list()

            batch_size = int(
                math.ceil(float(len(preList))/float(num_process)))
            print("batch_size:{}".format(batch_size))
            task_list = []

            p = multiprocess.Process(target=listener, args=(
               record,len(preList),start,lock))
            task_list.append(p)
            p.start()
            for i in range(num_process):
                tmp_pre = preList[i*batch_size:(i+1)*batch_size]
                tmp_text = textList[i*batch_size:(i+1)*batch_size]
                p = multiprocess.Process(target=sub_process, args=(tmp_text,tmp_pre,result,record,lock,i))
                task_list.append(p)
                p.start()
            for t in task_list:
                t.join()
        
            w=0
            n=0
            for (key,value) in tqdm(result):
                w+=key
                n+=value
                # print(n)
            print('{} \n total char：{} CER: {:.3f}'.format(pre[:-7],n,w/float(n)))
