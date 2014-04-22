# -*- coding: utf-8 -*-
from sendmsg import *

#点击菜单栏事件
def handle_click(key):
    #使用帮助
    if key == 'V1001_HELP':
        use_help()
    #热门活动
    elif key == 'V1001_TODAT_ACTIVE':
        hot_activity()
    #讲座信息
    elif key == 'V1001_TODAT_LECTURE':
        recent_lecture()
    #校园新闻
    elif key == 'V1001_SCHOOL_NEWS':
        school_news()
    #社团和部门信息
    elif key == 'V1001_OGNIZATION':
        school_club()
    elif key == 'V1001_MODERN_FIGURE':
        school_figure()

#用户输入文字信息处理
def handle_text(msg):
    if msg == u'活动':
        hot_activity()
    elif msg == u'讲座':
        recent_lecture()
    elif msg == u'新闻':
        school_news()
    elif msg == u'社团':
        school_club()
    elif msg == u'部门':
        school_department()
    elif msg == u'人物':
        school_figure()
    #其他Query分析
    else:
        text_query(msg)

#对用户消息分类处理
def handle_msg(xml):
    global content, template_type
    type = xml.find('MsgType').text
    if type == 'text':
        msg = xml.find('Content').text
        handle_text(msg)
    elif type == 'event':
        event = xml.find('Event').text
        if event == 'subscribe':
            use_help()
        elif event == 'CLICK':
            key = xml.find('EventKey').text
            handle_click(key)
    elif type == 'voice':
        content = '抱歉，暂时不支持语音消息'
        template_type = 'text'
    else:
        content = '抱歉，不支持此类型功能'
        template_type = 'text'