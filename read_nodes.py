# import sys
# sys.path.append("..")

from utils.wenzi2pinyin import wenzi2pinyin
import pandas as pd
from Convertor import Convertor
from os import path


nodesFile = "./nodes/math_nodes.txt"


def read_keyNouns(file):
    df = pd.read_csv(file, encoding="utf-8", sep="\t")
    titles = df["title"]
    dict = []
    convertor = Convertor()

    for _, title in titles.items():

        result, words = convertor.convert(title)  # title需要去掉标点符号
        result = result[0]  # result肯定都是只有一个元素的list
        if len(words[0])>1:
            keyNouns = KeyNouns(words[0], result.pinyin, result.yindiao)
            dict.append(keyNouns)

    # for key,value in dict.items():
    #     print(key)

    return dict


class KeyNouns:
    def __init__(self, words, pinyin, yindiao):
        self.words = words
        self.pinyin = pinyin
        self.yindiao = yindiao


if __name__ == "__main__":
    read_keyNouns(nodesFile)
