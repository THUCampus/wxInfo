# -*- coding: utf-8 -*-
from TuanTuan.TuanTuanApp.participle import *
from TuanTuan.TuanTuanApp.TextHandler.activity_handler import ActivityHandler
from TuanTuan.TuanTuanApp.TextHandler.club_handler import ClubHandler
from TuanTuan.TuanTuanApp.TextHandler.department_handler import DepartmentHandler
from TuanTuan.TuanTuanApp.TextHandler.lecture_handler import LectureHandler
from TuanTuan.TuanTuanApp.TextHandler.news_handler import NewsHandler
from TuanTuan.TuanTuanApp.TextHandler.common import get_mark_keywords
import time

########################################################################
class TextProcess:
    """输入用户发送的信息对象，输出要回复的信息对象"""

    #----------------------------------------------------------------------
    def __init__(self, inputText='', tags=[]):
        """Constructor"""
        self.inputText = inputText
        self.tags = tags
    
    #----------------------------------------------------------------------
    def process(self):
        """分词"""
        participle = Participle(self.inputText)
        participleResult = participle.getAccurate()
        """创建Handler"""
        clubHandler = ClubHandler(data=participleResult, rawInput=self.inputText, tags=self.tags)
        departmentHandler = DepartmentHandler(data=participleResult, rawInput=self.inputText, tags=self.tags)
        activityHandler = ActivityHandler(data=participleResult, rawInput=self.inputText, tags=self.tags)
        lectureHandler = LectureHandler(data=participleResult, rawInput=self.inputText, tags=self.tags)
        newsHandler = NewsHandler(data=participleResult, rawInput=self.inputText, tags=self.tags)
        """处理针对特定handler的查询"""
        relevance = {
            'st':clubHandler,
            'bm':departmentHandler,
            'hd':activityHandler,
            'jz':lectureHandler,
            'xw':newsHandler
        }
        result = None
        for name in relevance.keys():
            if name in self.tags:
                result = relevance[name].handle(current=[])
                break
        """没有针对特定的handler查询，则设定通用的顺序并处理"""
        if result == None:
            clubHandler.nextHandler = departmentHandler
            departmentHandler.nextHandler = activityHandler
            activityHandler.nextHandler = lectureHandler
            lectureHandler.nextHandler = newsHandler
            newsHandler.nextHandler = None
            result = clubHandler.handle(current=[])
        """对结果排序"""
        for each in result:
            if each['name'] == 'Lecture' or each['name'] == 'Activity':
                listbefore = []
                listafter = []
                for eachdata in each['data']:
                    if eachdata.act_time.strftime('%Y-%m-%d') >= time.strftime("%Y-%m-%d", time.localtime(time.time())):
                        listafter.append(eachdata)
                    else:
                        listbefore.append(eachdata)
                listafter.sort(key=lambda obj:obj.act_time, reverse=False)
                listbefore.sort(key=lambda obj:obj.act_time, reverse=True)
                each['data'] = listafter + listbefore
            elif each['name'] == 'News':
                newslist = []
                for eachdata in each['data']:
                    if eachdata.time.strftime('%Y-%m-%d') <= time.strftime("%Y-%m-%d", time.localtime(time.time())):
                        newslist.append(eachdata)
                newslist.sort(key=lambda obj:obj.time, reverse=True)
                each['data'] = newslist
        result.sort(key=lambda obj:obj.get('mark'), reverse=True)
        """去掉与第一个mark差距比较大的结果"""
        max_mark = result[0]['mark']
        len_result = len(result)
        position = 0
        while position < len_result:
            if result[position]['mark'] < max_mark - 3.999 or result[position]['mark'] < max_mark * 0.58:
                break
            position += 1
        result = result[0:position]
        """去掉匹配度过低的结果"""
        mark_keywords = get_mark_keywords(participleResult)
        for i in range(len(result)):
            if result[i]['mark'] < mark_keywords * 0.48 or (result[i]['mark'] < 1.999 and mark_keywords > 1):
                result[i]['data'] = []
        return result
