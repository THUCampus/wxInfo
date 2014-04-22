# -*- coding: utf-8 -*-
__author__ = 'jianglinnan'

import string
import jieba
import datetime

#分词类
class Participle:
    def __init__(self,text = ''):
        self.text = text

    #获取搜索模式分词结果
    def getAll(self):
        allWords = []
        allWords += jieba.cut_for_search(self.text)
        return allWords
    
    #获取精确模式分词结果
    def getAccurate(self):
        words = []
        words += jieba.cut(self.text,cut_all=False)
        return words


#时间处理类
class TimeProcess:
    #构造函数，输入为分词后列表
    def __init__(self,words = []):
        self.words = words
        self.splitUncommonWords(self.words)
        index = 0
        for each in self.words:
            index += 1
            if (each == u'日') and len(self.words) > index:
                if self.words[index] != ' ':
                    self.words.insert(index, ' ')
            if each == u'：':
                self.words[index-1] = u':'

    #获取输入串中的时间，并格式化时间
    #这是一个接口
    #输入串为12月6日，返回[['2013-12-06 00:00:00'],['2013-12-06 23:59:59']]
    def getTimes(self):
        times = []
        i = [0,0]
        j = 0
        times.append([])
        while i[0] < len(self.words):
            if self.recurTime(i,times[j]):
                times.append([])
                j = j + 1
        return self.timeFormat(times)

    #格式化时间
    #输入的为[['2013','y','05'],[06,'d']]格式的时间列表
    #返回一个[开始时间列表,结束时间列表]
    def timeFormat(self,time = []):
        ftime = []
        startTime = []
        endTime = []
        currentYear = datetime.datetime.now().strftime('%Y')
        currentMonth = datetime.datetime.now().strftime('%m')          
        for each in time:
            length = len(each)
            if (':' not in each and 'h' not in each) or ('d' in each) :
                if(length > 4):
                    startTime.append(each[0] + '-' + each[2] + '-' + each[4])
                    endTime.append(each[0] + '-' + each[2] + '-' + each[4])
                elif (length > 2):
                    if(string.atoi(each[0]) >= 2000):
                        startTime.append(each[0] + '-' + each[2] + '-01')
                        endTime.append(each[0] + '-' + each[2] + '-' + self.lastDay(each[0],each[2]))
                    elif(string.atoi(each[0]) <=12 and string.atoi(each[0]) >= 1):
                        year = datetime.datetime.now().year
                        month = datetime.datetime.now().strftime('%m')
                        if each[0] in ['01','02','03'] and month in['10','11','12'] :
                            year = str(year+1)
                        else:
                            year = str(year)                        
                        startTime.append(year+'-'+each[0]+'-'+each[2])
                        endTime.append(year+'-'+each[0]+'-'+each[2])
                    else:
                        pass
                elif(length == 2):
                    if each[1] == 'm':
                        year = datetime.datetime.now().year
                        month = datetime.datetime.now().strftime('%m')
                        if each[0] not in ['01','02','03','04','05','06','07','08','09','10','11','12']:
                            continue
                        elif each[0] in ['01','02','03'] and month in['10','11','12'] :
                            year = str(year+1)
                        else:
                            year = str(year)
                        startTime.append(year+'-'+each[0]+'-01')
                        endTime.append(year + '-' + each[0] + '-' + self.lastDay(year,each[0]))
                    elif each[1] == 'd':
                        startTime.append(currentYear+'-'+currentMonth+'-'+each[0])
                        endTime.append(currentYear+'-'+currentMonth+'-'+each[0])
                else:
                    continue
            else:
                if(length > 4):
                    startTime.append(each[0] + ':' + each[2] + ':' + each[4])
                    endTime.append(each[0] + ':' + each[2] + ':' + each[4])
                elif(length > 2):
                    startTime.append(each[0]+ ':' + each[2] + ':00')
                    endTime.append(each[0]+ ':' + each[2] + ':59')
                elif length == 2 and each[1] == 'h':
                    startTime.append(each[0]+ ':00:00')
                    endTime.append(each[0]+ ':59:59')
                else:
                    continue
        ftime.append(startTime)
        ftime.append(endTime)
        return ftime

    #提取特定的时间关键词
    def extraTime(self,result):
        """不支持形如'下个月4日'的查询"""
        time_exists = False
        if len(result['start']) != 0:
            time_exists = True
        """查询关键词"""
        for each in self.words:
            startDay = ''
            endDay = ''
            if each.encode('utf-8') == u'今天'.encode('utf-8'):
                startDay = datetime.datetime.now().strftime('%Y-%m-%d')
                endDay = startDay
            elif each.encode('utf-8') == u'明天'.encode('utf-8'):
                startDay = (datetime.datetime.now().date() + datetime.timedelta(1)).strftime('%Y-%m-%d')
                endDay = startDay
            elif each.encode('utf-8') == u'后天'.encode('utf-8'):
                startDay = (datetime.datetime.now().date() + datetime.timedelta(2)).strftime('%Y-%m-%d')
                endDay = startDay
            elif each.encode('utf-8') == u'本月'.encode('utf-8'):
                year = datetime.datetime.now().strftime('%Y')
                month = datetime.datetime.now().strftime('%m')
                startDay = year + '-' + month + '-01'
                endDay = year + '-' + month + '-' + self.lastDay(year,month)
            elif each.encode('utf-8') == u'下个月'.encode('utf-8'):
                year = datetime.datetime.now().date().year
                month = datetime.datetime.now().date().month
                if(month == 12):
                    month = '01'
                    year = str(year+1)
                startDay = year + '-' + month + '-01'
                endDay = year + '-' + month + '-' + self.lastDay(year,month)
            else:
                continue
            #检查是否已经包括时间，如果不包括，则加入时间
            if time_exists == False:
                result['start'].append(datetime.datetime.strptime(startDay + " " + "00:00:00", '%Y-%m-%d %H:%M:%S'))
                result['end'].append(datetime.datetime.strptime(endDay + " " + "23:59:59", '%Y-%m-%d %H:%M:%S'))
                time_exists = True
                continue
            else:
                result['start'] = []
                result['end'] = []
                return

    #递归地搜索输入串中的时间
    def recurTime(self,index,List):
        if index[0] >= len(self.words):
            return False
        if  not self.checkNum(self.words[index[0]]):
            index[0] += 1
            index[1] = 0
            return False
        else:
            tmp = self.words[index[0]]
            if len(tmp) == 1:
                tmp = '0' + tmp
            List.append(tmp)
            if self.DateProcess(index,List) == 1:
                index[0] += 2
                index[1] = 1                       
                self.recurTime(index,List)
                return True
            elif self.DateProcess(index,List) == 0:
                index[0] += 2
                index[1] = 0
                return True
            else:
                return True

    #协助递归处理时间，提取时间关键词
    def DateProcess(self,index,List):
        if(index[0]+1 >= len(self.words)):
            index[0] += 1
            return -1
        tmp = self.words[index[0]+1].encode("utf-8")
        flag = index[1]
        if (tmp in [each.encode("utf-8") for each in [u'年',u'月',u'日',u'/',u'-']]) and (flag == 1 or flag == 0):
            if(tmp == u'年'.encode("utf-8")):
                List.append('y')
            elif(tmp == u'月'.encode("utf-8")):
                List.append('m') 
            elif(tmp == u'日'.encode("utf-8")):
                List.append('d') 
            else:
                List.append('-')        
            return 1               
        elif (tmp in [each.encode("utf-8") for each in [u'时',u'分',u'秒',u'点',u':']]) and (flag == 1 or flag == 0):
            if tmp == u'点'.encode("utf-8") or tmp == u'时'.encode("utf-8"):
                List.append('h')
            else:
                List.append(':')          
            return 1               
        else:
            return 0
        
    #获得某年某月的最后一天
    def lastDay(self,year,month):
        if month in ['01','03','05','07','08','10','12']:
            return '31'
        elif month in ['04','06','09','11']:
            return '30'
        elif month == '02':
            yearInt = string.atoi(year)
            if yearInt % 4 != 0 or (yearInt % 100 == 0 and yearInt % 400 != 0):
                return '28'
            else: 
                return '29'        

    #判断一个字符串是否为纯数字
    def checkNum(self,s):
        nums = ['0','1','2','3','4','5','6','7','8','9']
        for each in s:
            if each not in nums:
                return False
        return True
    
    #处理日至，日到等特殊分词问题
    def splitUncommonWords(self, val = []):
        index = 0
        while index < len(val):
            if(val[index] == u'日至'):
                val[index] = u'日'
                val.insert(index+1, u'至')
                index += 2
            elif(val[index] == u'日到'):
                val[index] = u'日'
                val.insert(index+1, u'到')
                index += 2
            else:
                index += 1
