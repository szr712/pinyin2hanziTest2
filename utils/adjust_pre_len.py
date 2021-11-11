from utils.wenzi2pinyin import wenzi2pinyin
from Convertor import ishan
import time
import traceback
import requests
from utils.diff import diff

proxies = {'https': 'http://127.0.0.1:7078'}


def adjust_pre_len(pre_pinyin, text_pinyin, pre_result):
    """通过重新请求的方式，调整API请求结果的长度，使API请求结果与原文完全对齐

    Args:
        pre_pinyin (list): API请求结果的拼音list
        text_pinyin (list): 原文的拼音list
        pre_result (str): API请求结果的汉字

    Returns:
        str: 调整长度后的API请求结果，使其与原文等长
    """
    flag=1
    while flag != 0 and flag <= 10:
        try:
            pre_result=ishan(pre_result) # 去除英文縮寫的影響
            pre_pinyin,_=wenzi2pinyin(pre_result)
            if len(pre_pinyin) == len(text_pinyin):
                return pre_result
            differences = list(diff(pre_pinyin, text_pinyin))
            for i1, i2, j1, j2, a, b in differences:
                # print("{} {} {}".format(i1,i2,a))
                # print("{} {} {}".format(j1,j2,b))
                if len(a) != len(b):
                    sub=""
                    for word in b:
                        data_dict = {
                            'text': word,
                            'itc': "zh-t-i0-pinyin",
                            'num': 10,
                            'ie': "utf-8",
                            'oe': "utf-8' -H 'content-length:0'",
                        }
                        response = requests.post(
                            url='https://inputtools.google.com/request', data=data_dict, proxies=proxies)
                        # response = requests.post(
                        #     url='https://inputtools.google.com/request', data=data_dict)
                        candidates = response.json()[1][0][1]
                        for candidate in candidates:
                            if len(candidate) == 1:
                                sub=sub+candidate
                                break
                    pre_result=pre_result[:j1]+sub+pre_result[j1+len(a):]
        except Exception as e:
            flag += 1
            traceback.print_exc()
            print("Error")
            print(flag)
            if flag == 10:
                return ""
            time.sleep(1)
    if len(pre_result)>len(text_pinyin):
        pre_result=pre_result[:len(text_pinyin)]
    return pre_result
