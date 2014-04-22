# -*- coding: utf-8 -*-
from TuanTuan.TuanTuanApp.models import Club
from TuanTuan.TuanTuanApp.TextHandler.common import *
########################################################################
class ClubHandler:
    """处理社团消息"""

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
        all_data = Club.objects.all()
        """mark用来标记匹配的数量"""
        mark = {'mark' : 0}
        if ('dd' not in self.tags) and get_accurate_location(self.rawInput) == "":
            result = filter_name__contains(all_data, self.data, mark)
        else:
            result = set()
        """加入返回结果"""
        current.append({
            'name':'Club', 
            'data':list(result),
            'mark':mark['mark']
        })        
        """本层处理完毕，如果有必要，交给下一层处理"""
        if self.nextHandler != None and needNextFlag == True:
            return self.nextHandler.handle(current=current)
        else:
            return current

