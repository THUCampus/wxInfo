# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from handle import *
import hashlib
import xml.etree.ElementTree as ET
from django.views.decorators.csrf import csrf_exempt

def validate(request):
    signature =  request.GET.get("signature")
    timestamp = request.GET.get("timestamp")
    nonce = request.GET.get("nonce")
    token = 'TsinghuaChatToken'
    tmpArr = [token, timestamp, nonce]
    tmpArr.sort()
    tmpStr = ''.join(tmpArr)
    tmpStr = hashlib.sha1(tmpStr).hexdigest()
    if tmpStr == signature:
        return 1;
    else:
        return 0;

@csrf_exempt
def entry(request):
    #POST消息
    if request.method == 'POST':
        recvmsg = request.body
        xml = ET.fromstring(recvmsg)
        handle_msg(xml)
        return send_msg(request, xml)
    #access token
    elif request.GET.get("signature"):
        if validate(request) == 1:
            return HttpResponse(request.GET.get('echostr'))
        else:
            return HttpResponse('false')
    else:
         return HttpResponseRedirect("http://student.tsinghua.edu.cn/")

#活动界面逻辑与渲染
def activity_page(request):
    if request.GET.get('id'):
        id = request.GET.get('id')
        _activity = Activity.objects.get(id = id)
        variables = RequestContext(request, {'activity': _activity})
        return render_to_response('activity.html', variables)
    else:
        return render_to_response('activity.html')

#讲座界面逻辑与渲染
def lecture_page(request):
    if request.GET.get('id'):
        id = request.GET.get('id')
        lecture = Lecture.objects.get(id = id)
        variables = RequestContext(request, {'lecture': lecture})
        return render_to_response('lecture.html', variables)
    else:
        return render_to_response('lecture.html')

#新闻界面逻辑与渲染
def news_page(request):
    if request.GET.get('id'):
        id = request.GET.get('id')
        news = News.objects.get(id = id)
        variables = RequestContext(request, {'news': news})
        return render_to_response('news.html', variables)
    else:
        return render_to_response('news.html')

def club_page(request):
    if request.GET.get('id'):
        id = request.GET.get('id')
        club = Club.objects.get(id = id)
        variables = RequestContext(request, {'club': club})
        return render_to_response('club.html', variables)
    else:
        return render_to_response('club.html')

def department_page(request):
    if request.GET.get('id'):
        id = request.GET.get('id')
        department = Department.objects.get(id = id)
        variables = RequestContext(request, {'department': department})
        return render_to_response('department.html', variables)
    else:
        return render_to_response('department.html')

def figure_page(request):
    if request.GET.get('id'):
        id = request.GET.get('id')
        figure = ModernFigure.objects.get(id = id)
        variables = RequestContext(request, {'figure': figure})
        return render_to_response('figure.html', variables)
    else:
        return render_to_response('figure.html')



