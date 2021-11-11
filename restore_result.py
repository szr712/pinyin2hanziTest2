from Convertor import ishan
import os
import difflib
from utils.adjust_pre_len import adjust_pre_len
from utils.diff import diff
from pypinyin import pinyin
import pypinyin
from utils.wenzi2pinyin import wenzi2pinyin
from tqdm import tqdm

def restore_sen(pre,ori):
    """恢复API请求结果的非中文字符

    Args:
        pre (str): API请求结果
        ori (str): 原句 带有非中文字符

    Returns:
        tuple(str,str): 恢复标点的API请求结果;去除LaTeX公式的原句
    """
    oripre=pre
    oriori=ori

    pre=pre.replace("\n", "")
    ori=ori.replace("\n","")
    # 去公式
    if '$' in ori:
        tmpList = ori.split('$')
        ori = "".join(tmpList[::2]) 
    text=ishan(ori)
    differences = list(diff(text, ori))
    # print("pre:{}\nori:{}".format(text,ori))
    for i1, i2, j1, j2, a, b in differences:
        print("{} {} {}".format(i1,i2,a))
        print("{} {} {}".format(j1,j2,b))
        pre=pre[:j1]+b+pre[j1+len(a):]
        text=text[:j1]+b+text[j1+len(a):]

    # # 恢复公式
    # differences = list(diff(text, oriori))
    # for i1, i2, j1, j2, a, b in differences:
    #     pre=pre[:j1]+b+pre[j1+len(a):]
    #     text=text[:j1]+b+text[j1+len(a):]

    if len(pre)!=len(ori):
        print(oripre)
        print("pre:{}\nori:{}".format(pre,ori))
    return pre,text


def restore_result(preFileDir, oriFileDir, restoreFileDir,woLatexDir):
    """恢复API请求结果中的非中文字符，并将恢复结果按文件存入restoreFileDir
        同时去除原文件的LaTeX公式，存入woLatexDir目录下
        
    Args:
        preFileDir (str): API请求结果文件目录
        oriFileDir (str): 原文件目录
        restoreFileDir (str): 恢复标点后的存储目录
        woLatexDir (str): 去除原文件LaTeX公式后的存储目录
    """
    for oriFile in os.listdir(oriFileDir):
        with open(os.path.join(oriFileDir, oriFile), "r", encoding="utf-8") as fw:
            oriContents = fw.readlines()
        with open(os.path.join(preFileDir, oriFile+"pre.txt"), "r", encoding="utf-8")as fw:
            preContents = fw.readlines()
        result=[]
        texts=[]
        for pre,ori in tqdm(zip(preContents,oriContents)):
            a,b=restore_sen(pre,ori)
            result.append(a)
            texts.append(b)
        with open(os.path.join(restoreFileDir, oriFile+"_restore.txt"), "w", encoding="utf-8") as fw:
            for line in result:
                # print(line)
                fw.write(line+"\n")
        with open(os.path.join(woLatexDir, oriFile), "w", encoding="utf-8") as fw:
            for line in texts:
                # print(line)
                fw.write(line+"\n")

            # print(a,b)

def adjust_requst_result(preFileDir,textFileDir,dctDir):
    """调整已经存入本地的请求结果至等长

    Args:
        preFileDir (str): 预测结果目录
        textFileDir (str): 原文字目录
        dctDir (str): 目标目录
    """
    for preFile in os.listdir(preFileDir):
        print(preFile)
        adjust_result=[]
        with open(os.path.join(preFileDir, preFile), "r", encoding="utf-8")as fw:
            preContents = fw.readlines()
        with open(os.path.join(textFileDir, preFile[:-7]+"_text.txt"), "r", encoding="utf-8")as fw:
            textContents = fw.readlines()
        for pre,text in tqdm(zip(preContents,textContents)):
            pre=pre.replace("\n", "")
            text=text.replace("\n","")
            pre_pinyin, _ = wenzi2pinyin(pre)
            text_pinyin,_=wenzi2pinyin(text)
            pre=adjust_pre_len(pre_pinyin,text_pinyin,pre)
                # print("pre:{}text:{}".format(pre,text))
            adjust_result.append(pre)
        with open(os.path.join(dctDir, preFile), "w", encoding="utf-8")as fw:
            for line in tqdm(adjust_result):
                    fw.write(line+"\n")

def test_result_len_equal(preFileDir,textFileDir):
    total=0
    notEqual=0
    corrector=0
    for preFile in os.listdir(preFileDir):
        print(preFile)
        with open(os.path.join(preFileDir, preFile), "r", encoding="utf-8")as fw:
            preContents = fw.readlines()
        with open(os.path.join(textFileDir, preFile[:-7]+"_text.txt"), "r", encoding="utf-8")as fw:
        # with open(os.path.join(textFileDir, preFile+"_restore.txt"), "r", encoding="utf-8")as fw:
            textContents = fw.readlines()
        for pre,text in zip(preContents,textContents):
            total+=1
            if len(pre)!=len(text):
                # pre_pinyin, _ = wenzi2pinyin(pre)
                # text_pinyin,_=wenzi2pinyin(text)
                # pre=pre.replace("\n", "")
                # text=text.replace("\n","")
                # oripre=pre
                # pre=adjust_pre_len(pre_pinyin,text_pinyin,pre)
                notEqual+=1
                if len(pre)==len(text):
                    corrector+=1
                print("pre:{}text:{}".format(pre,text))
        #         print("pre:{}\ntext:{}\noripre:{}".format(pre,text,oripre))
        # print("total:{} notEqual:{}corrector:{}".format(total,notEqual,corrector))
        print("total:{} notEqual:{}".format(total,notEqual))

# def diff(a, b):
#     for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b).get_opcodes():
#         if tag!='equal':
#             yield a[i1:i2], b[j1:j2]


# def adjust_pre_len(preList,textList):
#     for pre,text in zip(preList,textList):
#         # for a,b in zip(pre,text):
#             # aList=pinyin(a,heteronym=True,style=pypinyin.NORMAL)
#             # bList=pinyin(b,heteronym=True,style=pypinyin.NORMAL)
#             # flag=0
#             # for i in bList[0]:
#             #     if i in aList[0]:
#             #         flag=1
#             #         break
#             # if not flag:
#             #     print("pre:{}text:{}".format(pre,text))
#             #     print("a:{} b:{}".format(a,b))
#         pre_pinyin, _ = wenzi2pinyin(pre)
#         text_pinyin,_=wenzi2pinyin(text)
#         # if len(pre)==len(text):

#         if pre_pinyin!=text_pinyin:
#             print("pre:{}text:{}".format(pre,text))
#             # print("a:{} b:{}".format(a,b))
#             result=list(diff(pre_pinyin,text_pinyin))
#             print(result)
#             # for a,b in zip(pre_pinyin,text_pinyin):
#             #     if a!=b:
#             #         print("pre:{}text:{}".format(pre,text))
#             #         print("a:{} b:{}".format(a,b))
#             #         result=list(diff(a,b))
#             #         print(result)
        

if __name__=="__main__":
    sen="平定大小和卓叛乱放弃对新疆的主权管辖我认为这种想法是完全错误的就像左宗棠说的一样新疆是中国的西北大门若馨将尸首沙俄南下塞外无险可守塞内试讲险象环生"
    test="（1）平定大小和卓叛乱。放弃对新疆的主权管辖。我认为这种想法是完全错误的，就像左宗棠说的一样，新疆是中国的西北大门，若新疆失守，沙俄南下，塞外无险可守，塞内势将险象环生。"
    a,b=restore_sen(sen,test)
    print(sen)
    print(a)


    # test_result_len_equal("./testFile","./restoreFile")
    # sen="若p真q假，则$\left\{ \begin{array}{l}{m＞2} \\ {m≤1或m≥3} \end{array} \right.$，解可得m≥3；"
    # print(sen)
    # print(repr(restore_sen("若真假则节课的",sen)))
    # restore_result("./preFile","./testFile","./restoreFile","./testFileWoLatex")
    # adjust_requst_result("./preFile","./textFile","./test")
    # for preFile in os.listdir("./preFile"):
    #     with open(os.path.join("./preFile", preFile), "r", encoding="utf-8")as fw:
    #         preContents = fw.readlines()
    #     with open(os.path.join("./textFile", preFile[:-7]+"_text.txt"), "r", encoding="utf-8")as fw:
    #         textContents = fw.readlines()
    #     for pre,text in zip(preContents,textContents):
    #         pre=pre.replace("\n", "")
    #         oripre=pre
    #         text=text.replace("\n", "")
    # pre = "在我国风蚀荒漠化多见于西北地区水时荒漠化多分布于南方低山丘陵和西南卡死特地去盐渍化主要分布在西北干旱灌溉渠和华北办事run驱动图荒漠化发生的青藏高原地区"
    # print(pre)
    # oripre=pre
    # text= "在我国风蚀荒漠化多见于西北地区水蚀荒漠化多分布于南方低山丘陵和西南喀斯特地区盐渍化主要分布在西北干旱灌溉区和华北半湿润区冻土荒漠化发生的青藏高原地区"

    # pre_pinyin, _ = wenzi2pinyin(pre)
    # text_pinyin,_=wenzi2pinyin(text)
    # print(pre_pinyin,text_pinyin)
    # # if len(pre_pinyin)!=len(text_pinyin):
    # pre=adjust_pre_len(pre_pinyin,text_pinyin,pre)
    # print("text:{}\npre:{}\nori:{}".format(text,pre,oripre))

