import re
from utils.wenzi2pinyin import wenzi2pinyin


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
    print (result_list)
    return result_list

if __name__=="__main__":
    adjust_sentence_len(150,"【探究资料】三级阶梯]部分水电站分布昆仑山一邦连山内蒙古第一级阶梯匕第三级阶{400mm北京800mm年降水量]1600mmC1月平均气温图335【尝试探究】(1)地形对河流的影响：我国多数河流自西向东注入太平洋，原因是许多大型水利枢纽工程建在abc河流流经的阶梯交界处，是因为(2)气候对河流的影响：我国秦岭淮河一线以北的河流冬季有结冰CD现象，主要原因是同端是树。我国东部e季风区的河流，深受季风气候的影响。秦岭淮河线以北的河流水量(填”大于”或”小于”)秦岭淮河一线以南的河流。(3)植被对河流的影响：秦岭淮河一线以南地区植被，河流含沙量小。【归纳总结】河流的特点可以从流向、水位、流量。含沙量有无结冰期等方面分析。这里河流的特点与气候、地形和植被等因素有密切关系。知识点是：台湾岛。")
