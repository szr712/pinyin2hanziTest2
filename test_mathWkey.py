"""
多进程测试Google API，带数学关键词
关键词修正后的结果存在newpre
"""
import math
import os
import re
from utils.findAll_keyNouns import findAll_keyNouns
from read_nodes import read_keyNouns

import multiprocess
from tqdm import tqdm

from Convertor import Convertor
from request_google import requset_google
import time

num_process = 128
testFilePath = "./testFile"


def sub_process(data, predic, textdic, lock, resdic, newresdic, newpre, keyNouns, batch_size, start, id):
    convertor = Convertor()
    for i, (index, line) in enumerate(data.items()):
        # print(index)
        pinyin, wenzi = convertor.convert(line)

        pre = ""
        new = ""
        key = []
        for chip in pinyin:
            result = requset_google(chip.pinyin, chip.yindiao)
            newResult = result

            # 关键字匹配
            for keyNoun in keyNouns:
                indexs = findAll_keyNouns(
                    chip.pinyin, chip.yindiao, keyNoun.pinyin, keyNoun.yindiao)
                for x in indexs:
                    newResult = newResult[:x]+keyNoun.words + \
                        newResult[x+len(keyNoun.pinyin):]
                    key.append(keyNoun.words)

            pre += result
            new += newResult

        lock.acquire()
        textdic[index] = "".join(wenzi)
        predic[index] = pre
        newpre[index] = new
        if pre != "".join(wenzi):
            resdic[index] = (pre, "".join(wenzi))
        if pre != new:
            newresdic[index] = (new, pre, "".join(wenzi), " ".join(key))
        # print("{}:{:.2f}%,  time:{:.2f}m".format(id,i/float(batch_size)*100,time.time()-start/60))
        lock.release()
    # print("end!!!!! rest:{}".format(id))


def listener(predic, total_size, start, lock):
    now = start
    while 1:
        # print(time.time()-now)
        if time.time()-now > 30:
            now = time.time()
            lock.acquire()
            print("{}/{}, {:.2f}%, cost:{:.2f}m,rest:{:.2f}m".format(len(predic), total_size, float(len(predic)) /
                  total_size*100, (time.time()-start)/60, (time.time()-start)/60/(float(len(predic)/total_size))-(time.time()-start)/60))
            lock.release()
        if total_size-len(predic) < 100:
            break


if __name__ == "__main__":

    fileList = os.listdir(testFilePath)

    lock = multiprocess.Lock()

    keyNouns = read_keyNouns("./nodes/math_nodes.txt")

    for file in fileList:
        start = time.time()
        print("fileName:{}".format(file))
        with multiprocess.Manager() as m:

            predic = m.dict()
            textdic = m.dict()
            resdic = m.dict()
            newresdic = m.dict()
            newpre = m.dict()

            with open(os.path.join(testFilePath, file), "r", encoding="utf-8") as fw:
                contents = fw.readlines()

            batch_size = int(
                math.ceil(float(len(contents))/float(num_process)))
            print("batch_size:{}".format(batch_size))

            data = {v: k for v, k in enumerate(contents)}

            task_list = []

            p = multiprocess.Process(target=listener, args=(
                predic, len(contents), start, lock))
            task_list.append(p)
            p.start()

            for i in range(num_process):
                tmp_data = dict(list(data.items())[
                                i*batch_size:(i+1)*batch_size])
                p = multiprocess.Process(target=sub_process, args=(
                    tmp_data, predic, textdic, lock, resdic, newresdic, newpre, keyNouns, batch_size, start, i))
                task_list.append(p)
                p.start()
            for t in task_list:
                t.join()

            print("start save")
            with open(os.path.join("./textFile", file+"_text.txt"), 'w', encoding='utf-8') as f:
                for key in tqdm(sorted(textdic.keys())):
                    f.write(textdic[key]+"\n")

            with open(os.path.join("./preFile", file+"pre.txt"), 'w', encoding='utf-8') as f:
                for key in tqdm(sorted(predic.keys())):
                    f.write(predic[key]+"\n")

            with open(os.path.join("./newpre", file+"new.txt"), 'w', encoding='utf-8') as f:
                for key in tqdm(sorted(newpre.keys())):
                    f.write(newpre[key]+"\n")

            with open(os.path.join("./comparison", file+"_result.txt"), 'w', encoding='utf-8') as f:
                for key in tqdm(sorted(resdic.keys())):
                    f.write(("pre:{}\ntar:{}\n\n").format(
                        resdic[key][0], resdic[key][1]))

            with open(os.path.join("./comparison", file+"_newresult.txt"), 'w', encoding='utf-8') as f:
                for key in tqdm(sorted(newresdic.keys())):
                    f.write(("new:{}\npre:{}\ntar:{}\nkeyNouns{}\n\n").format(
                        newresdic[key][0], newresdic[key][1], newresdic[key][2], newresdic[key][3]))
                        
            print("total time:{:.2f}m".format((time.time()-start)/60))
