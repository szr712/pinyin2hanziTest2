import os
from request_google import requset_google
from tqdm import tqdm
from Convertor import Convertor

testFilePath = "./testFile"
fileList = os.listdir(testFilePath)

for file in fileList:
    print("fileName:{}".format(file))
    with open(os.path.join(testFilePath, file), "r", encoding="utf-8") as fw:
        contents = fw.readlines()

    convertor = Convertor()
    text = ""
    pre = ""
    for line in tqdm(contents):
        pinyin, wenzi = convertor.convert(line)
        text = text+"".join(wenzi)+"\n"
        for chip in pinyin:
            result = requset_google(chip.pinyin, chip.yindiao)
            pre += result
        pre += "\n"
    with open(os.path.join("./textFile", file+"_text.txt"), 'w', encoding='utf-8') as f:
        f.write(text)
    with open(os.path.join("./preFile", file+"pre.txt"), 'w', encoding='utf-8') as f:
        f.write(pre)
