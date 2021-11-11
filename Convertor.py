from zhon.hanzi import punctuation
import string
from utils.wenzi2pinyin import wenzi2pinyin

def ishan(text):
    """去除输入字符串中除中文字符串的内容

    Args:
        text (str): 字符串

    Returns:
        str: 去除非中文字符后的字符串
    """
    # for python 3.x
    # sample: ishan('一') == True, ishan('我&&你') == False

    result= [char if '\u4e00' <= char and char<= '\u9fff' else "" for char in text]
    return "".join(result)

class Convertor:

    class Sentence:
        def __init__(self):
            self.pinyin = []
            self.yindiao = []

    def convert(self, oriList):
        """将字符串转换成可请求的格式

        Args:
            oriList (str): 输入字符串

        Returns:
            list: 一个Sentence类的list，Sentence类内涵拼音及对应的音调
            list: 去除输入字符串中非中文字符的list，list内每个元素长度小于30
        """

        result=[]

        if '$' in oriList:
            tmpList = oriList.split('$')
            oriList = "".join(tmpList[::2])  # 去除公式部分

        splitList = []

        while len(oriList) > 20:
            i = 1
            for i in range(1, 20):
                if oriList[20-i] in string.punctuation or oriList[20-i] in punctuation:
                    break
            if i==19:
                splitList.append(ishan(oriList[:20]))
                oriList = oriList[20:]
            else:
                splitList.append(ishan(oriList[:21-i]))
                oriList = oriList[21-i:]
        splitList.append(ishan(oriList))
        
        for chip in splitList:
            # print(chip)
            pinyinList,toneList=wenzi2pinyin(chip)
            sen=self.Sentence()
            sen.pinyin=pinyinList
            sen.yindiao=toneList
            result.append(sen)
        return result,splitList

if __name__=="__main__":
    text="究发现酸的浓度越大，产生气体的速度越快，与甲比较，对丁分析正确的是    （填编号）。"
    convertor=Convertor()
    result,list=convertor.convert(text)
    # print(list)
    for r in result:
        print(r.pinyin,"len:{}".format(len(r.pinyin)))
        print(r.yindiao,"len:{}".format(len(r.yindiao)))