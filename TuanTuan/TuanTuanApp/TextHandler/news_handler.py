# -*- coding: utf-8 -*-
from TuanTuan.TuanTuanApp.models import News
from TuanTuan.TuanTuanApp.TextHandler.common import *
from TuanTuan.TuanTuanApp.participle import *
########################################################################
class NewsHandler:
    """处理新闻消息"""

    #----------------------------------------------------------------------
    def __init__(self, data=[], rawInput='', tags=[]):
        """Constructor"""
        self.data = data
        self.rawInput = rawInput
        self.tags = tags
        self.nextHandler = None

    #----------------------------------------------------------------------
    def handle(self, current=[]):
        """标记是否需要继续处理"""
        needNextFlag = True
        """本层进行处理"""
        all_data = News.objects.all()
        time = {'start' : [], 'end' : []}
        result = set()
        """mark用来标记匹配的数量"""
        mark_title = {'mark' : 0}
        mark_time = {'mark' : 0}
        mark = {'mark' : 0}
        """如果输入的是精确地点，则忽略，因为新闻没有地点"""
        if get_accurate_location(self.rawInput) == "":
            """过滤分词结果中的无用部分"""
            filter_keywords_result = filter_keywords(self.data, self.tags)
            """统计去除无用部分之后的总字数"""
            mark_keywords = get_mark_keywords(filter_keywords_result)
            """初始化查询结果"""
            query_title = set()
            query_time = set()
            """首先进行标题的匹配"""
            if 'sj' not in self.tags:
                query_title = filter_title__contains(all_data, filter_keywords_result, mark_title)
            """然后进行时间的匹配"""
            if 'bt' not in self.tags:
                timeProcess = TimeProcess(words = self.data)
                time = time_merge(timeProcess.getTimes())
                timeProcess.extraTime(time)
                query_time = filter_time(all_data, time, key = 'news')
                if len(query_time) != 0:
                    mark_time['mark'] = len(time['start']) * 4
            """进行结果的处理，如果标题全部匹配上，只考虑标题"""
            if mark['mark'] == mark_keywords and mark['mark'] != 0 and len(query_time) == 0:
                result = query_title
            else:
                result = query_title
                """如果检测到有输入时间，则输入的时间一定是用来限制结果的"""
                if len(time['start']) != 0 and len(filter_keywords_result) != 0:
                    result = result & query_time
                if len(time['start']) != 0 and len(filter_keywords_result) == 0:
                    result = query_time
        """根据两个部分的mark确定结果的mark"""
        if mark_title['mark'] >= mark_time['mark']:
            mark['mark'] = mark_title['mark'] + mark_time['mark'] * 0.2
        else:
            mark['mark'] = mark_time['mark'] + mark_title['mark'] * 0.2
        """加入返回结果"""
        current.append({
            'name':'News', 
            'data':list(result),
            'mark':mark['mark']
        })
        """本层处理完毕，如果有必要，交给下一层处理"""
        if self.nextHandler != None and needNextFlag == True:
            return self.nextHandler.handle(current=current)
        else:
            return current
