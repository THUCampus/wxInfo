# -*- coding: utf-8 -*-
from TuanTuan.TuanTuanApp.models import Lecture
from TuanTuan.TuanTuanApp.TextHandler.common import *
from TuanTuan.TuanTuanApp.participle import *
########################################################################
class LectureHandler:
    """处理讲座消息"""

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
        all_data = Lecture.objects.all()
        time = {'start' : [], 'end' : []}
        """mark用来标记匹配的数量"""
        mark = {'mark' : 0}
        mark_title = {'mark' : 0}
        mark_site = {'mark' : 0}
        mark_time = {'mark' : 0}
        """尝试获得精确地点，如果是精确地点，则进行精确地点的匹配"""
        accurate_location = get_accurate_location(self.rawInput)
        if accurate_location != "" and check_same_in_list(['bt', 'sj'], self.tags) == False:
            result = match_accurate_location(all_data, accurate_location)
            if len(result) != 0:
                mark_site['mark'] = len(self.rawInput)
        else:
            """过滤分词结果中的无用部分"""
            filter_keywords_result = filter_keywords(self.data, self.tags)
            """统计去除无用部分之后的总字数"""
            mark_keywords = get_mark_keywords(filter_keywords_result)
            """初始化查询结果"""
            query_title = set()
            query_site = set()
            query_time = set()
            """首先进行标题的匹配"""
            if check_same_in_list(['dd', 'sj'], self.tags) == False:
                query_title = filter_title__contains(all_data, filter_keywords_result, mark_title)
            """然后进行地点的匹配"""
            if check_same_in_list(['bt', 'sj'], self.tags) == False:
                query_site = filter_site__contains(all_data, filter_keywords_result, mark_site)
            """最后进行时间的匹配"""
            if check_same_in_list(['bt', 'dd'], self.tags) == False:
                timeProcess = TimeProcess(words = self.data)
                time = time_merge(timeProcess.getTimes())
                timeProcess.extraTime(time)
                query_time = filter_time(all_data, time)
                if len(query_time) != 0:
                    mark_time['mark'] = len(time['start']) * 4
            """进行结果的处理，如果标题全部匹配上，只考虑标题，如果地点全部匹配上，只考虑地点"""
            if mark_title['mark'] == mark_keywords and mark_title['mark'] != 0 and len(query_time) == 0:
                result = query_title
            elif mark_site['mark'] == mark_keywords and mark_site['mark'] != 0 and len(query_time) == 0:
                result = query_site
            else:
                result = query_title & query_site
                if len(result) == 0:
                    result = query_title | query_site
                """如果检测到有输入时间，则输入的时间一定是用来限制结果的"""
                if len(time['start']) != 0 and len(filter_keywords_result) != 0:
                    result = result & query_time
                if len(time['start']) != 0 and len(filter_keywords_result) == 0:
                    result = query_time
        """根据三个部分的mark确定结果的mark"""
        if mark_title['mark'] >= mark_site['mark'] and mark_title['mark'] >= mark_time['mark']:
            mark['mark'] = mark_title['mark'] + mark_site['mark'] * 0.2 + mark_time['mark'] * 0.2
        elif mark_site['mark'] >= mark_title['mark'] and mark_site['mark'] >= mark_time['mark']:
            mark['mark'] = mark_site['mark'] + mark_title['mark'] * 0.2 + mark_time['mark'] * 0.2
        else:
            mark['mark'] = mark_time['mark'] + mark_title['mark'] * 0.2 + mark_site['mark'] * 0.2
        """加入返回结果"""
        current.append({
            'name':'Lecture', 
            'data':list(result),
            'mark':mark['mark']
        })
        """本层处理完毕，如果有必要，交给下一层处理"""
        if self.nextHandler != None and needNextFlag == True:
            return self.nextHandler.handle(current=current)
        else:
            return current

