import os
import random
from sklearn.model_selection import train_test_split
import regex
import re
from tqdm import tqdm
import itertools
from Convertor import ishan
import concurrent.futures

from utils.wenzi2pinyin import wenzi2pinyin

testFilePath = "./testFile"
fileList = os.listdir(testFilePath)
test_set_path="test_set_pinyin_to_character_model"

def adjust_sentence_len(max_len,sentence):
    pinyin_list,_=wenzi2pinyin(sentence)
    if len("".join(pinyin_list))<max_len:
        return [sentence]
    # split_dot=["。","！","？"]
    tmp_list = re.sub(u"(?<=([。！？]))", r"|", sentence).split("|")
    result_list=[]
    for line in tmp_list:
        pinyin_tmp,_=wenzi2pinyin(line)
        if len("".join(pinyin_tmp))<max_len:
            result_list.append(line)
        else:
            tmp=re.sub(u"(?<=([。，！？]))", r"|", sentence).split("|")
            for i in tmp:
                p,_=wenzi2pinyin(i)
                if(len("".join(p)))<max_len:
                    result_list.append(i)
    result_list=[a for a in result_list if len(ishan(a))>2]
    return result_list
    
    

def clean(text):
    # if regex.search("[A-Za-z0-9]", text) is not None: # For simplicity, roman alphanumeric characters are removed.
    # # if regex.search("[A-Za-z0-9]", text) is not None: # For simplicity, roman alphanumeric characters are removed.
    #     return ""

    # 去除公式
    if '$' in text:
        tmpList = text.split('$')
        text = "".join(tmpList[::2]) 
    # text = regex.sub(u"[^ \p{\u4e00-\u9fa5}A-Za-z0-9\"{}\\(\\)\\[\\]\\*&.?!,…:;\u3002|\uff1f|\uff01|\uff0c|\u3001|\uff1b|\uff1a|\u201c|\u201d|\u2018|\u2019|\uff08|\uff09|\u300a|\u300b|\u3008|\u3009|\u3010|\u3011|\u300e|\u300f|\u300c|\u300d|\ufe43|\ufe44|\u3014|\u3015|\u2026|\u2014|\uff5e|\ufe4f|\uffe5]\+\-\*\/\=", "", text)
    text = regex.sub(u"[^ \p{\u4e00-\u9fa5}A-Za-z0-9\"{}\\(\\)\\[\\]\\*&.?!,…:;\u3002|\uff1f|\uff01|\uff0c|\u3001|\uff1b|\uff1a|\u201c|\u201d|\u2018|\u2019|\uff08|\uff09|\u300a|\u300b|\u3008|\u3009|\u3010|\u3011|\u300e|\u300f|\u300c|\u300d|\ufe43|\ufe44|\u3014|\u3015|\u2026|\u2014|\uff5e|\ufe4f|\uffe5]", "", text)
    text_new=text
    # flag=0
    # for char in text:
    #     if char !="。" and char !="，" and char !="！" and char!="？":
    #         flag=0
    #         text_new=text_new+char
    #     elif not flag:
    #         flag=1
    #         text_new=text_new+char
    text_new=text_new.replace(" ","")
    text_new=text_new.replace("\t","")
    text_new=text_new.replace("\n","")
    
    # while "，，" in text:
    #     text=text.replace("，，","，")
    if len(ishan(text_new))<=2: return ""
    return adjust_sentence_len(150,text_new)

if __name__=="__main__":

    total_train_set=[]

    for file in fileList:
        print(file)
        with open(os.path.join(testFilePath,file),"r",encoding="utf-8") as f:
            contents=f.readlines()

        # lines=[re.sub(u"(?<=([。！？]))", r"|", clean(l)).split("|") for l in tqdm(contents)]
        # for line in tqdm(contents):
        #     line=clean(line)
        #     lines=re.sub(u"(?<=([。，！？]))", r"|", line).split("|")
        # print("len(lines):{}".format(len(lines)))
        # data_set=list(itertools.chain.from_iterable(lines))
        # with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        #     res = list(tqdm(executor.map(clean, contents),total=len(contents)))
            
        data_set=[clean(l) for l in tqdm(contents)]
        # data_set=list(res)
        data_set=list(itertools.chain.from_iterable(data_set))
        data_set = [x for x in data_set if x != '']

            # print("+++++++++")
            # contents=[clean(i) for i in contents]
            # contents = [i for i in contents if len(i) <= 100 and len(i)>=10 and "$" not in i and "\t" not in i]

        # selected=random.sample(contents,100)
        train_set, test_set = train_test_split(data_set, test_size=0.3, random_state=42)
        total_train_set=total_train_set+train_set
        print(len(test_set))

        if len(test_set)>3000:
            random.seed(42)
            test_set = random.sample(test_set, 3000)
            print(len(test_set))

        with open(os.path.join(test_set_path,file),"w",encoding="utf-8") as f:
            for i,line in enumerate(test_set):
                # f.write("{}\t{}\n".format(i,line))
                f.write("{}\n".format(line))
        with open(os.path.join(test_set_path,file[:-4]+"_pinyin.txt"),"w",encoding="utf-8") as f:
            total_test_set_pinyin=[]
            for line in tqdm(test_set):
                pinyin_list,_=wenzi2pinyin(line)
                total_test_set_pinyin.append("".join(pinyin_list))
            # total_train_set_pinyin=[wenzi2pinyin(x) for x in tqdm(total_train_set)]
            f.writelines("\n".join(total_test_set_pinyin))

    with open("train_set.txt","w",encoding="utf-8") as f:
        f.writelines("\n".join(total_train_set))
        # for i,line in tqdm(enumerate(total_train_set)):
        #     # f.write("{}\t{}\n".format(i,line))
        #     f.write("{}\n".format(line))

    with open("train_set_pinyin.txt","w",encoding="utf-8") as f:
        total_train_set_pinyin=[]
        for line in tqdm(total_train_set):
            pinyin_list,_=wenzi2pinyin(line)
            total_train_set_pinyin.append("".join(pinyin_list))
        # total_train_set_pinyin=[wenzi2pinyin(x) for x in tqdm(total_train_set)]
        f.writelines("\n".join(total_train_set_pinyin))
        # for i,line in tqdm(enumerate(total_train_set_pinyin)):
        #     # f.write("{}\t{}\n".format(i,line))
        #     f.write("{}\n".format(line))

