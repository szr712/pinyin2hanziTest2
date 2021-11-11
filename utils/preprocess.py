# -*- coding: UTF-8 -*-
from zhon.hanzi import punctuation
import string

def preprocess_data(oriContents,restoreContents):
    """预处理数据，使其最长长度不大于500个字符

    Args:
        oriContents (list)): 原文list
        restoreContents (list): 恢复标点后的API请求结果list

    Returns:
        tuple(list,list): 符合长度限制的原文list,符合长度要求的请求结果list
    """
    ori_processed=[]
    restore_processed=[]
    for ori,res in zip(oriContents,restoreContents):
        while len(ori) > 500:
            i = 1
            for i in range(1, 500):
                if ori[500-i] in string.punctuation or ori[500-i] in punctuation:
                    break
            if i==499:
                ori_processed.append(ori[:500])
                restore_processed.append(res[:500])
                ori = ori[500:]
                res=res[500:]
            else:
                ori_processed.append(ori[:501-i])
                restore_processed.append(res[:501-i])
                ori = ori[501-i:]
                res=res[501-i:]
        ori_processed.append(ori)
        restore_processed.append(res)
    return ori_processed,restore_processed

if __name__=="__main__":
    ori_processed,restore_processed=preprocess_data(["材料一世界反法西斯战争把世界正义的力量团结在一起，各国人民为捍卫和平奋起反  击法西斯亲绿。苏德战场是反法西斯战争的重要战场之一。中国战场是反法西斯战争的东方主战场，是打败日本法西斯的决定性力量。反法西斯战争孕育了反法西斯精神。传承反法西斯精神和抗战精神，具有 重大历史意义和现实意义。材料二戰後，欧洲传统的国际地位一落千丈，无论是战胜国还是战败国，杜伦威尔、三流国家。美、苏以欧洲为主战场的“冷战”， 更是欧洲人民终于意识到再也不能发生欧洲人打欧洲人的战争了。（1）材料一中“世界正义的力量团结在一起”，决定建立联合国是那次会议？（2）根据教材 ，请写出苏联为世界反法西斯战争作出重大贡献的战役一粒？（3）卢沟桥事变后，国共两党共赴国难，抗日民族统一战线正式建立。这是国共两党第几次合作？（4）材料二中“冷战”开始的标志是什么？（5）为了不再“发生欧洲人大欧洲人的战争”，西欧在欧共体的基础上，建立起的区域合作组织是什么？这个组织 的出现，推动世界政治格局吵什么趋势发展？（6）今年是世界反法西斯战争暨抗日战争胜利多少周年？（7）传承反法西斯精神和抗战精神，具有重大意义。 结合所学知识，谈谈你对抗战精神的理解？"],["材料一世界反法西斯战争把世界正义的力量团结在一起，各国人民为捍卫和平奋起反  击法西斯侵略。苏德战场是反法西斯战争的重要战场之一。中国战场是 反法西斯战争的东方主战场，是打败日本法西斯的决定性力量。反法西斯战争孕育了反法西斯精神。传承反法西斯精神和抗战精神，具有重大历史意义和现实 意义。材料二战后，欧洲传统的国际地位一落千丈，无论是战胜国还是战败国，都沦为二、三流国家。美、苏以欧洲为主战场的“冷战”，更使欧洲人民终于意 识到再也不能发生欧洲人打欧洲人的战争了。（1）材料一中“世界正义的力量团结在一起”，决定建立联合国是哪次会议？（2）根据教材，请写出苏联为世界 反法西斯战争作出重大贡献的战役一例？（3）卢沟桥事变后，国共两党共赴国难，抗日民族统一战线正式建立。这是国共两党第几次合作？（4）材料二中“冷战”开始的标志是什么？（5）为了不再“发生欧洲人打欧洲人的战争”，西欧在欧共体的基础上，建立起的区域合作组织是什么？这个组织的出现，推动世界政 治格局朝什么趋势发展？（6）今年是世界反法西斯战争暨抗日战争胜利多少周年？（7）传承反法西斯精神和抗战精神，具有重大意义。结合所学知识，谈谈你对抗战精神的理解？"])

    for a,b in zip(ori_processed,restore_processed):
        print(a+"\n")
        print(b+"\n")

