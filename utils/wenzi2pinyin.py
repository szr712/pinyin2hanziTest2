from typing import Text
from pypinyin import Style, pinyin
from pypinyin.core import lazy_pinyin


def wenzi2pinyin(text):
    pinyin_list = lazy_pinyin(text, style=Style.TONE3)
    # print(pinyin_list)
    tones_list = [int(py[-1]) if py[-1].isdigit()
                else 0 for py in pinyin_list]
    pinyin_list = lazy_pinyin(text, style=Style.NORMAL)
    return pinyin_list, tones_list

if __name__=="__main__":
    # text="【探究资料】三级阶梯]部分水电站分布昆仑山一邦连山内蒙古第一级阶梯匕第三级阶{400mm北京800mm年降水量]1600mmC1月平均气温图335【尝试探究】(1)地形对河流的影响：我国多数河流自西向东注入太平洋，原因是许多大型水利枢纽工程建在abc河流流经的阶梯交界处，是因为(2)气候对河流的影响：我国秦岭淮河一线以北的河流冬季有结冰CD现象，主要原因是同端是树。我国东部e季风区的河流，深受季风气候的影响，秦岭淮河线以北的河流水量(填”大于”或”小于”)秦岭淮河一线以南的河流。(3)植被对河流的影响：秦岭淮河一线以南地区植被，河流含沙量小。【归纳总结】河流的特点可以从流向、水位、流量。含沙量有无结冰期等方面分析。这里河流的特点与气候、地形和植被等因素有密切关系。知识点是：台湾岛。"
    text="角色,角度"
    pinyin_list,_=wenzi2pinyin("角色,角度")
    print(pinyin_list)