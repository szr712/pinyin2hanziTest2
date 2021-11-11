import os
from utils.preprocess import preprocess_data
from utils.diff import diff
from tqdm import tqdm
import json
import random
from sklearn.model_selection import train_test_split


def make_dataset(restoreFileDir, oriFileDir, dstDir):
    """制作bert数据集，数据集分为train、test、dev，分割比例为9:1

    Args:
        restoreFileDir (str): 恢复标点后的API请求结果目录
        oriFileDir (str): 原文目录
        dstDir (str):数据集存储目录
    """
    dataset = []
    for oriFile in os.listdir(oriFileDir):
        with open(os.path.join(oriFileDir, oriFile), "r", encoding="utf-8") as fw:
            oriContents = fw.readlines()
        with open(os.path.join(restoreFileDir, oriFile+"_restore.txt"), "r", encoding="utf-8")as fw:
            restoreContents = fw.readlines()

        oriContents,restoreContents=preprocess_data(oriContents,restoreContents)

        for res, ori in tqdm(zip(restoreContents, oriContents)):

            # 去公式
            # if '$' in ori:
            #     tmpList = ori.split('$')
            #     ori = "".join(tmpList[::2])

            res = res.replace("\n", "")
            ori = ori.replace("\n", "")

            # 去空格
            res = res.replace(" ", "")
            ori = ori.replace(" ", "")

            if res=="" or ori=="":
                continue

            if len(res)!=len(ori):
                print(res)

            # differences = list(diff(res, ori))

            # for i1, i2, j1, j2, a, b in differences:
            #     if i1!=j1 or i2!=j2:
            #         print("res:{}\nori:{}\n".format(res,ori))
            #         print("a:{},b:{}\n".format(a,b))

            wrong_ids = []

            for i, (a, b) in enumerate(zip(res, ori)):
                if a != b:
                    wrong_ids.append(i)

            data_dict = {
                "id": "-",
                "original_text": res,
                "wrong_ids": wrong_ids,
                "correct_text": ori
            }
            if len(res)>500:
                print("{}\n{}\n".format(res,ori))
            dataset.append(data_dict)

    train_set, test_set = train_test_split(dataset, test_size=0.1, random_state=42)
    print(len(train_set))
    print(len(test_set))

    sum=0
    for i in train_set:
        if len(i["wrong_ids"])!=0:
            sum+=1
    print(sum)
    sum=0
    for i in test_set:
        if len(i["wrong_ids"])!=0:
            sum+=1
    print(sum)


    with open(os.path.join(dstDir, 'train_edu.json'), 'w', encoding="utf-8") as f:
        json.dump(train_set, f, ensure_ascii=False)
    with open(os.path.join(dstDir, 'dev_edu.json'), 'w', encoding="utf-8") as f:
        json.dump(test_set, f, ensure_ascii=False)
    with open(os.path.join(dstDir, 'test_edu.json'), 'w', encoding="utf-8") as f:
        json.dump(test_set, f, ensure_ascii=False)


def make_dataset2(restoreFileDir, oriFileDir, dstDir):
    """制作bert数据集，数据集分为train、test、dev，分割比例为9:1,
        以句号作为分割

    Args:
        restoreFileDir (str): 恢复标点后的API请求结果目录
        oriFileDir (str): 原文目录
        dstDir (str):数据集存储目录
    """
    dataset = []
    for oriFile in os.listdir(oriFileDir):
        with open(os.path.join(oriFileDir, oriFile), "r", encoding="utf-8") as fw:
            oriContents = fw.readlines()
        with open(os.path.join(restoreFileDir, oriFile+"_restore.txt"), "r", encoding="utf-8")as fw:
            restoreContents = fw.readlines()

        ori_sen=[]
        res_sen=[]
        for ori,pre in zip(oriContents,restoreContents):
            ori=ori.split("。")
            pre=pre.split("。")
            for a,b in zip(ori,pre):
                if len(a)==0:
                    continue
                ori_sen.append(a+"。")
                res_sen.append(b+"。")

        oriContents,restoreContents=preprocess_data(ori_sen,res_sen)

        for res, ori in tqdm(zip(restoreContents, oriContents)):

            # 去公式
            # if '$' in ori:
            #     tmpList = ori.split('$')
            #     ori = "".join(tmpList[::2])

            res = res.replace("\n", "")
            ori = ori.replace("\n", "")

            # 去空格
            res = res.replace(" ", "")
            ori = ori.replace(" ", "")

            if res=="" or ori=="":
                continue

            if len(res)!=len(ori):
                print(res)

            # differences = list(diff(res, ori))

            # for i1, i2, j1, j2, a, b in differences:
            #     if i1!=j1 or i2!=j2:
            #         print("res:{}\nori:{}\n".format(res,ori))
            #         print("a:{},b:{}\n".format(a,b))

            wrong_ids = []

            for i, (a, b) in enumerate(zip(res, ori)):
                if a != b:
                    wrong_ids.append(i)

            data_dict = {
                "id": "-",
                "original_text": res,
                "wrong_ids": wrong_ids,
                "correct_text": ori
            }
            if len(res)>500:
                print("{}\n{}\n".format(res,ori))
            dataset.append(data_dict)

    train_set, test_set = train_test_split(dataset, test_size=0.1, random_state=42)
    print(len(train_set))
    print(len(test_set))

    sum=0
    for i in train_set:
        if len(i["wrong_ids"])!=0:
            sum+=1
    print(sum)
    sum=0
    for i in test_set:
        if len(i["wrong_ids"])!=0:
            sum+=1
    print(sum)


    with open(os.path.join(dstDir, 'train_edu_sen.json'), 'w', encoding="utf-8") as f:
        json.dump(train_set, f, ensure_ascii=False)
    with open(os.path.join(dstDir, 'dev_edu_sen.json'), 'w', encoding="utf-8") as f:
        json.dump(test_set, f, ensure_ascii=False)
    with open(os.path.join(dstDir, 'test_edu_sen.json'), 'w', encoding="utf-8") as f:
        json.dump(test_set, f, ensure_ascii=False)

if __name__ == "__main__":
    make_dataset2("./restoreFile", "./testFileWoLatex", "./bert_dataset")
