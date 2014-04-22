# -*- coding: utf-8 -*-
__author__ = 'thinkpad'
from TextHandler.entry import *
def exactquery(inputText):
    tags = []
    inputText = inputText.split(' ')
    Text = inputText[0:len(inputText)]
    if len(Text) > 1:
        for i in range(0,2):
            if Text[i] == 'st' or Text[i] == u'社团':
                inputText.remove(Text[i])
                tags.append('st')
            if Text[i] == 'bm' or Text[i] == u'部门':
                inputText.remove(Text[i])
                tags.append('bm')
            if Text[i] == 'hd' or Text[i] == u'活动':
                inputText.remove(Text[i])
                tags.append('hd')
            if Text[i] == 'jz' or Text[i] == u'讲座':
                inputText.remove(Text[i])
                tags.append('jz')
            if Text[i] == 'xw' or Text[i] == u'新闻':
                inputText.remove(Text[i])
                tags.append('xw')
            if Text[i] == 'bt' or Text[i] == u'标题':
                inputText.remove(Text[i])
                tags.append('bt')
            if Text[i] == 'dd' or Text[i] == u'地点':
                inputText.remove(Text[i])
                tags.append('dd')
            if Text[i] == 'sj' or Text[i] == u'时间':
                inputText.remove(Text[i])
                tags.append('sj')
    inputText = ''.join(inputText)
    return TextProcess(inputText, tags).process()
