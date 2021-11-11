"""
多进程测试
"""
import math
import os
from utils.wenzi2pinyin import wenzi2pinyin
from utils.adjust_pre_len import adjust_pre_len

import multiprocess
from tqdm import tqdm

from Convertor import Convertor
from request_google import requset_google
import time

num_process = 64
testFilePath = "./testset/original"


def sub_process(data, predic, textdic, lock, batch_size, start, id):
    convertor = Convertor()
    for i, (index, line) in enumerate(data.items()):
        # print(index)
        pinyin, wenzi = convertor.convert(line)

        pre = ""
        for chip, text in zip(pinyin, wenzi):
            result = requset_google(chip.pinyin, chip.yindiao)
            pre_pinyin, _ = wenzi2pinyin(result)
            text_pinyin, _ = wenzi2pinyin(text)
            result = adjust_pre_len(pre_pinyin, text_pinyin, result)
            pre += result

        lock.acquire()
        textdic[index] = "".join(wenzi)
        predic[index] = pre
        # print("{}:{:.2f}%,  time:{:.2f}m".format(id,i/float(batch_size)*100,time.time()-start/60))
        lock.release()


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

    for file in fileList:
        start = time.time()
        print("fileName:{}".format(file))
        with multiprocess.Manager() as m:

            predic = m.dict()
            textdic = m.dict()

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
                    tmp_data, predic, textdic, lock, batch_size, start, i))
                task_list.append(p)
                p.start()
            for t in task_list:
                t.join()

            print("start save")
            with open(os.path.join("./testset/expeted", file+"_text.txt"), 'w', encoding='utf-8') as f:
                for key in tqdm(sorted(textdic.keys())):
                    f.write(textdic[key]+"\n")
            with open(os.path.join("./testset/pre", file+"_pre.txt"), 'w', encoding='utf-8') as f:
                for key in tqdm(sorted(predic.keys())):
                    f.write(predic[key]+"\n")
            print("total time:{:.2f}m".format((time.time()-start)/60))
            print("average time:{:.2f}m".format((time.time()-start)/len(textdic)))
