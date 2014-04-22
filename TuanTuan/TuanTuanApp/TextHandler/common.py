# -*- coding: utf-8 -*-
import datetime
#----------------------------------------------------------------------
def get_best_matchs(matchs, mark):
    """根据已经抽象出的matchs(参见下边几个函数的代码)返回较好的匹配结果"""
    result = []
    """统计匹配的最好的条目匹配上的字数"""
    match_max = 0
    for each in matchs:
        if match_max < each['number']:
            match_max = each['number']
    mark['mark'] = match_max
    """将匹配比较好的条目加入到结果"""
    if match_max == 0:
        return []
    for each in matchs:
        if each['number'] >= match_max - 2 and each['number'] >= 0.68 * match_max:
            result.append(each['data'])    
    return result

#----------------------------------------------------------------------
def filter_name__contains(query, keywords, mark):
    """根据名字过滤查询结果，返回名字包含尽可能多的关键词的查询结果"""
    """获取每个query的标题与关键字匹配的数量"""
    matchs = [{'number':get_match_number(keywords, each.name), 'data':each} for each in query]
    result = get_best_matchs(matchs, mark);
    return set(result)

#----------------------------------------------------------------------
def filter_title__contains(query, keywords, mark):
    """根据标题过滤查询结果，返回标题包含尽可能多的关键词的查询结果"""
    """获取每个query的标题与关键字匹配的数量"""
    matchs = [{'number':get_match_number(keywords, each.title), 'data':each} for each in query]
    result = get_best_matchs(matchs, mark);
    return set(result)

#----------------------------------------------------------------------
def filter_site__contains(query, keywords, mark):
    """根据地点过滤查询结果，返回地点包含尽可能多的关键词的查询结果"""
    """获取每个query的地点与关键字匹配的数量"""
    matchs = [{'number':get_match_number(keywords, each.site), 'data':each} for each in query]
    result = get_best_matchs(matchs, mark);
    return set(result)

#----------------------------------------------------------------------
def filter_time(query, time, key = ''):
    """按照时间进行过滤"""
    if len(time['start']) == 0:
        return set()
    result = []
    """如果用户只输入了一个时间"""
    if len(time['start']) == 1:
        for each in query:
            if key == 'news': # 新闻部分的字段名不一样，是time而不是act_time
                if each.time >= time['start'][0].date() and each.time <= time['end'][0].date():
                    result.append(each)
            else:
                if each.act_time >= time['start'][0] and each.act_time <= time['end'][0]:
                    result.append(each)
    """如果用户输入超过两个时间"""
    if len(time['start']) >= 2:
        for each in query:
            if key == 'news': # 新闻部分的字段名不一样，是time而不是act_time
                if each.time >= time['start'][0].date() and each.time <= time['end'][1].date():
                    result.append(each)
            else:
                if each.act_time >= time['start'][0] and each.act_time <= time['end'][len(time['end'])-1]:
                    result.append(each) 
    return set(result)

#----------------------------------------------------------------------
def get_match_number(keywords, text):
    """获取text中有多少个keywords，返回所有keyword的长度之和"""
    count = 0
    for keyword in keywords:
        if text.find(keyword) != -1:
            count += len(keyword)
    return count

#----------------------------------------------------------------------
def get_accurate_location(text):
    """如果是一个精确的地点，则返回地点的标准格式，否则返回空字符串"""
    locations = {
        "新清华学堂":u"新清华学堂",
        "艺术教育中心":u"艺术教育中心",
        "艺教中心":u"艺术教育中心",
        "蒙民伟楼":u"艺术教育中心",
        "蒙民伟音乐厅":u"蒙民伟音乐厅",
        "大礼堂":u"大礼堂",
        "一教":u"一教",
        "1教":u"一教",
        "二教":u"二教",
        "2教":u"二教",
        "三教":u"三教",
        "3教":u"三教",
        "四教":u"四教",
        "4教":u"四教",
        "五教":u"五教",
        "5教":u"五教",
        "六教":u"六教",
        "6教":u"六教"
    }
    """如果匹配上了精确的地点，则进行匹配，否则返回空字符串"""
    if text.encode('utf-8') in locations.keys():
        return locations[text.encode('utf-8')]
    else:
        return ""

#----------------------------------------------------------------------
def match_accurate_location(query,text):
    """针对确认是地点的匹配函数"""
    result = []
    for each in query:
        if each.site.find(text) != -1:
            result.append(each)
    return set(result)

#----------------------------------------------------------------------
def filter_keywords(keywords, tags=[]):
    """过滤掉分词结果中无用的部分"""
    result = []
    """处理6教这种地点，防止被时间处理删掉"""
    for i in range(len(keywords)-1):
        if keywords[i] == u'1' and keywords[i+1].find(u'教') == 0:
            keywords[i+1] = u'一教'
        if keywords[i] == u'2' and keywords[i+1].find(u'教') == 0:
            keywords[i+1] = u'二教'
        if keywords[i] == u'3' and keywords[i+1].find(u'教') == 0:
            keywords[i+1] = u'三教'
        if keywords[i] == u'4' and keywords[i+1].find(u'教') == 0:
            keywords[i+1] = u'四教'
        if keywords[i] == u'5' and keywords[i+1].find(u'教') == 0:
            keywords[i+1] = u'五教'
        if keywords[i] == u'6' and keywords[i+1].find(u'教') == 0:
            keywords[i+1] = u'六教'
    """检查keywords中是否包含时间"""
    time_flag = False
    time_words = [u'年', u'月', u'日', u'点', u'-', u':', u'日至', u'日到', u'今天', u'明天', u'后天', u'本月', u'下个月']
    for each in keywords:
        if each in time_words:
            time_flag = True
            break
    """常见的搜索时输入的停用词，如果有时间，则去除时间"""
    stop_words = [u'的', u'在', u'从', u'到', u'有', u' ', u',', u'.', u'?', u'"', u'，', u'。', u'？', u'“', u'”']
    for each in keywords:
        if each not in stop_words:
            if time_flag == False or check_same_in_list(['bt', 'dd'], tags) == True or (each not in time_words and is_num(each) == False):
                result.append(each)
    return result

#----------------------------------------------------------------------
def get_mark_keywords(filter_keywords_result):
    """返回过滤后的关键词的总字数"""
    result = 0;
    for each in filter_keywords_result:
        result += len(each);
    return result

#----------------------------------------------------------------------
def check_same_in_list(list1, list2):
    """检查两个列表是否存在相同元素"""
    for each in list1:
        if each in list2:
            return True
    return False

#----------------------------------------------------------------------
def time_merge(time = []):
    """将处理后的时间列表转化成时间对象，处理日期和时间之间的关系"""
    result = {'start' : [], 'end' : []}
    try:
        i = 0
        while i < len(time[0]):
            # 如果上来遇到的是时间，则用当天的日期来补
            if time[0][i].find(':') != -1:
                sftime = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time[0][i]
                eftime = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time[1][i]
                start = datetime.datetime.strptime(sftime,'%Y-%m-%d %H:%M:%S')
                end = datetime.datetime.strptime(eftime,'%Y-%m-%d %H:%M:%S')
                i += 1
            # 如果最后遇到的是日期，则按整天计算
            elif i == len(time[0]) - 1 and time[0][i].find('-') != -1:
                start = datetime.datetime.strptime(time[0][i] + " " + "00:00:00", '%Y-%m-%d %H:%M:%S')
                end = datetime.datetime.strptime(time[1][i] + " " + "23:59:59", '%Y-%m-%d %H:%M:%S')
                i += 1
            # 如果遇到日期，且下一项为时间，则合并
            elif time[0][i].find("-") != -1 and time[0][i+1].find(':') != -1:
                start = datetime.datetime.strptime(time[0][i] + ' ' + time[0][i+1], '%Y-%m-%d %H:%M:%S')
                end = datetime.datetime.strptime(time[1][i] + ' ' + time[1][i+1], '%Y-%m-%d %H:%M:%S')
                i += 2
            # 其它情况，按整天计算
            else:
                start = datetime.datetime.strptime(time[0][i] + " " + "00:00:00", '%Y-%m-%d %H:%M:%S')
                end = datetime.datetime.strptime(time[1][i] + " " + "23:59:59", '%Y-%m-%d %H:%M:%S')
                i += 1
            result['start'].append(start)
            result['end'].append(end)
    except:
        pass
    return result

#----------------------------------------------------------------------
def is_num(s):
    """检查是否是非负整数"""
    nums = ['0','1','2','3','4','5','6','7','8','9']
    for each in s:
        if each not in nums:
            return False
    return True
