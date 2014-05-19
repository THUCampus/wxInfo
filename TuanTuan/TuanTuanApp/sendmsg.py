# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from TuanTuan.TuanTuanApp import *
from models import *
from ExactQuery import *
import time
import random

media_path = 'http://115.28.212.177:8000/static/img/upload/'

class result_url:
    title = ''
    picurl = ''
    url = ''
    def __init__(self, title, picurl, url):
        self.title = title
        self.picurl = picurl
        self.url = url

def use_help():
    global content, template_type
    content = '感谢使用请华学通社校园资讯平台！\n'
    content += '直接输入想要查询的内容即可进行模糊查询，若想进行精确查询请按照如下格式输入：\n'
    content += '活动查询：【HD 活动名称、地点或时间】\n'
    content += '讲座查询：【JZ 讲座名称、地点或时间】\n'
    content += '新闻查询：【XW 新闻名称或时间】\n'
    content += '课程查询：【KC 课程名称或地点】\n'
    content += '社团查询：【ST 社团名称】\n'
    content += '部门查询：【BM 部门名称】\n'
    content += '例--HD 清华新年音乐会\n'
    content += '您也可以点击菜单栏的按钮使用其他功能\n'
    template_type = 'text'

def hot_activity():
    global count, template_type, content, List
    activities = Activity.objects.all().order_by('-stick','act_time')
    List = []
    count = 0
    for each in activities:
        if each.act_time.strftime('%Y-%m-%d') >= time.strftime("%Y-%m-%d", time.localtime(time.time())):
            str = each.picurl.name
            if str[0:4] == 'http':
                List.append(result_url(title=each.title, picurl=each.picurl, url= local_url + 'activity/?id=' + str(each.id)))
            else:
                List.append(result_url(title=each.title, picurl=media_path + each.picurl.name, url= local_url + 'activity/?id=' + str(each.id)))
            count += 1
        if count > 3:
            break
    List.append(result_url(title='获取更多演出资讯', picurl='', url='http://tuan.ssast.org/u/helpact/'))
    count +=1
    template_type = 'list'

def recent_lecture():
    global count, template_type, content, List
    List = []
    count = 0
    lectures = Lecture.objects.all().order_by('-stick','act_time')
    for each in lectures:
        if each.act_time.strftime('%Y-%m-%d') >= time.strftime("%Y-%m-%d", time.localtime(time.time())):
            str = each.picurl.name
            if str[0:4] == 'http':
                List.append(result_url(title=each.title, picurl=each.picurl, url=local_url + 'lecture/?id=' + str(each.id)))
            else:
                List.append(result_url(title=each.title, picurl=media_path + each.picurl.name, url=local_url + 'lecture/?id=' + str(each.id)))
            count += 1
        if count > 3:
            break
    List.append(result_url(title='获取更多讲座预告', picurl='', url='http://tuan.ssast.org/u/helplecture/'))
    count +=1
    template_type = 'list'

def school_news():
    global count, template_type, content, List
    news = News.objects.all().order_by('-stick','-time')
    List = []
    count = 0
    for each in news:
        if each.time.strftime('%Y-%m-%d') <= time.strftime("%Y-%m-%d", time.localtime(time.time())):
            List.append(result_url(title=each.title, picurl=each.picurl, url=local_url + 'news/?id=' + str(each.id)))
            count += 1
        if count > 4:
            break
    template_type = 'list'

def school_figure():
    global count, template_type, content, List, wei_data
    figures = ModernFigure.objects.all()
    List = []
    length = len(figures)
    if length == 0:
        content = '对不起，目前没有人物信息'
        template_type = 'text'
    elif length == 1:
        count = 1
        wei_data = figures[0]
        template_type = 'figure'
    elif length < 3:
        count = length
        template_type = 'list'
        for figure in figures:
            List.append(result_url(title=figure.title, picurl=figure.picurl, url=local_url + 'figure/?id=' + str(figure.id)))
    else:
        count = 3
        template_type = 'list'
        figure_list = range(0,length)
        figureId = random.sample(figure_list, 3)
        for id in figureId:
            figure = figures[id]
            List.append(result_url(title=figure.title, picurl=figure.picurl, url=local_url + 'figure/?id=' + str(figure.id)))

def school_club():
    global count, template_type, content, List
    List = []
    clubs = Club.objects.all().order_by('-stick')
    length = len(clubs)
    if length < 4:
        count = length
        template_type = 'list'
        for club in clubs:
            List.append(result_url(title=club.name, picurl= club.picurl, url=local_url + 'club/?id=' + str(club.id)))
    else:
        count = 0
        template_type = 'list'
        for club in clubs:
            if club.stick > 0:
                List.append(result_url(title=club.name, picurl= club.picurl, url=local_url + 'club/?id=' + str(club.id)))
                count +=1
            else:
                break
            if count > 3:
                break
        if count < 4:
            club_list = range(count,length)
            clubId = random.sample(club_list, 4-count)
            for id in clubId:
                count += 1
                club = clubs[id]
                List.append(result_url(title=club.name, picurl=club.picurl, url=local_url + 'club/?id=' + str(club.id)))
    List.append(result_url(title='获取更多社团协会', picurl='', url='http://tuan.ssast.org/u/helpclub/'))
    count += 1

def school_department():
    global count, template_type, content, List, wei_data
    departments = Department.objects.all().order_by('-stick')
    List = []
    length = len(departments)
    if length == 0:
        content = '对不起，目前没有部门信息'
        template_type = 'text'
    elif length == 1:
        count = 1
        wei_data = departments[0]
        template_type = 'department'
    elif length < 5:
        count = length
        template_type = 'list'
        for department in departments:
            List.append(result_url(title=department.name, picurl=department.picurl, url=local_url + 'department/?id=' + str(department.id)))
    else:
        count = 0
        template_type = 'list'
        for department in departments:
            if department.stick > 0:
                List.append(result_url(title=department.name, picurl= department.picurl, url=local_url + 'club/?id=' + str(department.id)))
                count +=1
            else:
                break
            if count > 4:
                break
        if count < 5:
            department_list = range(count,length)
            departmentId = random.sample(department_list, 5-count)
            for id in departmentId:
                count += 1
                department = departments[id]
                List.append(result_url(title=department.name, picurl=department.picurl, url=local_url + 'department/?id=' + str(department.id)))

def text_query(msg):
    global count, template_type, content, List, wei_data
    #对字符串进行处理，返回查询结果
    content = ''
    result = exactquery(msg)
    List = []
    count = 0
    template_type = 'list'
    for each in result:
        count += len(each['data'])
    if count > 0:
        for each in result:
            if each['name'] == 'Activity':
                if count == 1 and len(each['data']) == 1:
                    wei_data = each['data'][0]
                    template_type = 'activity'
                    break
                else:
                    for tmp in each['data']:
                        List.append(result_url(title=tmp.title, picurl=tmp.picurl, url=local_url + 'activity/?id=' + str(tmp.id)))
            elif each['name'] == 'Lecture':
                if count == 1 and len(each['data']) == 1:
                    wei_data = each['data'][0]
                    template_type = 'lecture'
                    break
                else:
                    for tmp in each['data']:
                        List.append(result_url(title=tmp.title, picurl=tmp.picurl, url=local_url + 'lecture/?id=' + str(tmp.id)))
            elif each['name'] == 'News':
                if count == 1 and len(each['data']) == 1:
                    wei_data = each['data'][0]
                    template_type = 'news'
                    break
                else:
                    for tmp in each['data']:
                        List.append(result_url(title=tmp.title, picurl=tmp.picurl, url=local_url + 'news/?id=' + str(tmp.id)))
            elif each['name'] == 'Club':
                if count == 1 and len(each['data']) == 1:
                    wei_data = each['data'][0]
                    template_type = 'club'
                    break
                else:
                    for tmp in each['data']:
                        List.append(result_url(title=tmp.name, picurl=tmp.picurl, url=local_url + 'club/?id=' + str(tmp.id)))
            elif each['name'] == 'Department':
                if count == 1 and len(each['data']) == 1:
                    wei_data = each['data'][0]
                    template_type = 'department'
                    break
                else:
                    for tmp in each['data']:
                        List.append(result_url(title=tmp.name, picurl=tmp.picurl, url=local_url + 'department/?id=' + str(tmp.id)))
        if count > 5:
            count = 5
    #没有找到合适结果
    else:
        if content == '':
            content = '对不起，没有搜索到相关信息，请精确输入'
        template_type = 'text'

def send_msg(request, xml):
    global count, template_type, content, List, wei_data
    _to = xml.find('FromUserName').text
    _from = xml.find('ToUserName').text
    if template_type == 'text':
        variables = RequestContext(request, {'to':_to, 'from':_from, 'time':int(time.time()),'type':'text', 'content':content})
        return render_to_response('weixin_text.html', variables)
    elif template_type == 'list':
        variables = RequestContext(request, {'to':_to, 'from':_from, 'time':int(time.time()),'type':'news', 'count': count, 'list': List})
        return render_to_response('weixin_list.html', variables)
    else:
        variables = RequestContext(request, {'to':_to, 'from':_from, 'time':int(time.time()),'type':'news', 'count': count, 'local_url':local_url, template_type: wei_data})
        return render_to_response('weixin_' + template_type + '.html', variables)
