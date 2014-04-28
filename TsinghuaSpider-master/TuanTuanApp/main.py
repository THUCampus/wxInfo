# -*- coding: UTF-8 -*-
__author__ = 'Xu'

import os
import sys

os.environ.setdefault('SSAST_DEPLOYMENT', 'tuantuan')
path = os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/../'
if path not in sys.path:
    sys.path.insert(1, path)
os.environ['DJANGO_SETTINGS_MODULE'] = "ThuSpider.settings"
import urllib2
import urllib
import bs4
import re
import json
import string
from TuanTuanApp.models import *
from participle import *
import time

def getArtShowXML():
    url = 'http://www.hall.tsinghua.edu.cn/yczx.aspx'
    content = urllib2.urlopen(url).read()
    soup = bs4.BeautifulSoup(content)
    #find all <a> links
    mytable = soup.find_all('a')
    #server to post
    server = 'http://tuantuan.ssast.org/sql/activity/'

    #from 9th to 24th
    for item in range(9, 24, 1):
        link = mytable[item]['href']
        #search for id
        regex = re.search("[0-9]+", link)
        number = string.atoi(regex.group(0))
        content = urllib2.urlopen('http://www.hall.tsinghua.edu.cn/' + link).read()
        root = bs4.BeautifulSoup(content)
        #contents in the 5th table
        table = root.html.find_all('table')[5]
        table['width'] = "97%"
        table['height'] = ""
        tds = root.html.find_all(attrs = {"valign": "top"})
        for td in tds:
            td.extract()

        td = table.find_all('td')[0]
        td['width'] = "100%"

        picurl = 'http://www.hall.tsinghua.edu.cn' + table.img['src']
        for imgtag in table.find_all('img'):
            imgtag.extract()

        #<p> tags
        ptags = table.find_all('p')
        ptags[1].extract()
        ptags[2].extract()
        #title
        titlestr = ptags[3].text.split('\n')[0].encode('utf-8')
        title = titlestr[9:len(titlestr)]
        #time
        curtime = ptags[4].text.split('\n')[0][3:].encode('utf-8')
        try:
            a = title.decode('utf-8')
            b = curtime.decode('utf-8')
        except:
            continue
        a = title.decode('utf-8')
        #actor
        actor = ptags[5].text.encode('utf-8')
        #site
        site = ptags[4].text.split('\n')[2][3:].strip()
        site = site[3:].encode('utf-8')
        #ticket
        ticket = ptags[6].text.split('\n')[0].encode('utf-8')
        #access_time = ""
        val = str(table).replace('\xc2\xa0','')
        val = EnterDisplay(val)
        access_time = "1993-01-01"
        activity = Activity.objects.filter(title=title, act_time=curtime)
        if activity.count() == 0:
            try:
              Activity.objects.create(title=title, picurl=picurl, access_time=access_time, act_time=curtime, site=site,
                    actor=actor, ticket=ticket, content = val, stick = 0)
            except Exception, data:
                pass


def getTsinghuaNewsCharacter():
    rootUrl = 'http://news.tsinghua.edu.cn'
    urls = 'http://news.tsinghua.edu.cn/publish/news/4208/index.html'
    indexPage = urllib2.urlopen(urls)
    indexContent = indexPage.read()
    indexRoot = bs4.BeautifulSoup(indexContent)
    linklist = indexRoot.find('div', id = 'datalist_sec2').ul.findAll('li')
    for item in linklist:
        #title
        title = item.a.string.encode('utf-8')
        picurl = ''
        tmpUrl = item.a['href']
        page = urllib2.urlopen(rootUrl + tmpUrl)
        content = page.read()
        root = bs4.BeautifulSoup(content)
        #content
        htmlText = root.find('div', id = 'datalist_detail')
        #img
        imgs = htmlText.findAll('img')
        if len(imgs) > 0:
            if imgs[0]['src'][0:4] != 'http':
                picurl = rootUrl + imgs[0]['src']
            else:
                picurl =  imgs[0]['src']
        #summary
        summary = ''
        #time
        timeString =  root.find('div', id = 'title_detail_picwriter').string[4:14]
        news = News.objects.filter(title=title)
	print "insert one element"
        if len(news) == 0:
            try:
                News.objects.create(title=title, content=htmlText.encode('utf-8'), picurl=picurl, time=timeString, summary=summary, stick = 0)
            except:
                print "error"

def getTsinghuaNewsSynthesis():
    rootUrl = 'http://news.tsinghua.edu.cn'
    urls = 'http://news.tsinghua.edu.cn/publish/news/4205/index.html'
    indexPage = urllib2.urlopen(urls)
    indexContent = indexPage.read()
    indexRoot = bs4.BeautifulSoup(indexContent)
    linklist = indexRoot.find('div', id = 'datalist_sec2').ul.findAll('li')
    for item in linklist:
        #title
        title = item.a.string.encode('utf-8')
        picurl = ''
        tmpUrl = item.a['href']
        page = urllib2.urlopen(rootUrl + tmpUrl)
        content = page.read()
        root = bs4.BeautifulSoup(content)
        #content
        htmlText = root.find('div', id = 'datalist_detail')
        #img
        imgs = htmlText.findAll('img')
        if len(imgs) > 0:
            if imgs[0]['src'][0:4] != 'http':
                picurl = rootUrl + imgs[0]['src']
            else:
                picurl =  imgs[0]['src']
        #summary
        summary = ''
        #time
        timeString =  root.find('div', id = 'title_detail_picwriter').string[4:14]
        news = News.objects.filter(title=title)
        if len(news) == 0:
            try:
                News.objects.create(title=title, content=htmlText.encode('utf-8'), picurl=picurl, time=timeString, summary=summary, stick = 0)
            except Exception, data:
                print "error"

def getStudentTsinghuaNews():
    d1 = datetime.datetime.now()
    d3 = d1 - datetime.timedelta(days = 20)
    url1 = 'http://166.111.17.5:8080/getNews?'
    urlparam = {
        'start_time':d3.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time':d1.strftime('%Y-%m-%d %H:%M:%S'),
        'valid_code':'tuanwei'
    }
    sd = urllib.urlencode(urlparam)
    url2 = url1 + sd
    page = urllib2.urlopen(url2)

    #page = urllib2.urlopen('''http://166.111.17.5:8080/getNews?start_time=2013-11-10%2000:00:00&end_time=2013-12-21%2000:00:00&valid_code=tuanwei''')
    content = page.read()
    json_read = json.loads(content)
    if(json_read['result'] == 'success'):

        for item in json_read['news']:
            title = item['title'].encode('utf-8')
            content = item['content'].encode('utf-8')
            time = item['updatetime'].split('T')[0]
            summary = item['newAbstract'].encode('utf-8')
            soup = bs4.BeautifulSoup(content)
            picurl = ""

            ps = soup.find_all('p')
            #processing the style of p tags
            for p in ps:
                if 'style' not in p.attrs.keys():
                    p['style'] = 'background:none;'
                else:
                    p['style'] += '; background:none;'
                pimg = p.find_all('img')
                if len(pimg) != 0:
                    p['style'] += '; text-indent:0px'
            imgs = soup.find_all('img')
            if len(imgs) > 0:
                if imgs[0]['src'][0:4] != 'http':
                    picurl = 'http://student.tsinghua.edu.cn' + imgs[0]['src']
                else:
                    picurl =  imgs[0]['src']

            for img in imgs:
                img.parent.parent['style'] = 'line-height: 125%; text-align: center;'
                if img['src'][len(img['src'])-3: len(img['src'])] != 'gif':
                    img['style'] = "width:95%; border-radius: 8px; text-align: center;"
                    img['height'] = ""
                    img['width'] = ""
                if img['src'][0:4] != 'http':
                    img['src'] = 'http://student.tsinghua.edu.cn' + img['src']

            content = LastLineFormat(str(soup))
            news = News.objects.filter(title=title)
            if len(news) == 0:
                try:
                    News.objects.create(title=title, content=content, picurl=picurl, time=time, summary=summary, stick = 0)
                except Exception, data:
                    print "error"
    else:
        print 'error occured in read news'
'''
def getTsinghuaLecture():
    server = 'http://tuantuan.ssast.org/sql/lecture/'
    #server = 'http://127.0.0.1:8000/sql/lecture/'
    page = urllib2.urlopen("http://oars.tsinghua.edu.cn/zzh/30630.nsf/1de?ReadForm&Start=1&Count=50&Expand=2&TemplateType=2&TargetUNID=58F7D30CE9E69CFA482567B800261A8B&AutoFramed")
    content = page.read().decode('gb2312', 'ignore').encode('utf8')
    root = bs4.BeautifulSoup(content)
    linklist = root.findAll('a')

    for item in range(7,len(linklist)-2,2):
        if linklist[item].contents[0].encode('utf8').find('文化素质教育讲座') >= 0:
            link = linklist[item]['href']
            temp = link
            number = temp.split('/')[4]
            page = urllib2.urlopen("http://oars.tsinghua.edu.cn" + link)
            content = page.read().decode('gb2312', 'ignore').encode('utf8')
            root = bs4.BeautifulSoup(content)
            content = root.findAll('P')[0]
            hr = content.findAll('hr')
            for each in hr:
                each.extract()

            temp = str(content)
            temp = temp.split('\n')
            title = ""
            actor = '无'
            act_time = '2013-01-01'
            site = "清华大学"
            for each in temp:
                if each.find('演讲题目：') >= 0:
                    title ="《文化素质教育讲座》--" + each[15:len(each)]
                    title = endFormat(title)
                if each.find('第') >= 0 and each.find('讲 ') >= 0:
                    title ="《文化素质教育讲座》--" + each[0:len(each)]
                    title = endFormat(title)
                if each.find('第') >= 0 and each.find('期：') >= 0:
                    title ="《文化素质教育讲座》--" + each[0:len(each)]
                    title = endFormat(title)
                if each.find('演讲人：') >= 0:
                    actor = each[12:len(each)]
                    actor = endFormat(actor)
                if each.find('嘉  宾：') >= 0:
                    actor = each[11:len(each)]
                    actor = endFormat(actor)
                if each.find('主讲人：') >= 0:
                    actor = each[12:len(each)]
                    actor = endFormat(actor)
                if each.find('讲座嘉宾：') >= 0:
                    actor = each[15:len(each)]
                    actor = endFormat(actor)
                if each.find('时间：') >= 0:
                    act_time = each[9:len(each)]
                    act_time = endFormat(act_time)
                if each.find('时  间：') >= 0:
                    act_time = each[11:len(each)]
                    act_time = endFormat(act_time)
                if each.find('日期：') >= 0:
                    act_time = each[9:len(each)]
                    act_time = endFormat(act_time)
                if each.find('地点：') >= 0:
                    site = each[9:len(each)]
                    site = endFormat(site)
                if each.find('地  点：') >= 0:
                    site = each[11:len(each)]
                    site = endFormat(site)
            if title == "":
                title = '《文化素质教育讲座》--' + actor
            content = str(content)
            content = content.replace('</br>','')
            curtime = TimeProcess(Participle(act_time).getAll()).getTimes()
            act_time = curtime[0][0] + ' ' + curtime[0][1]
            access_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            lecture = Lecture.objects.filter(title=title)
            if lecture.count() == 0:
                try:
                    Lecture.objects.create(title=title, picurl='http://www.tsinghua.edu.cn/publish/th/campus/trees/view8.jpg', access_time=access_time, act_time=act_time, site=site,
                        actor=actor, content=content, stick = 0)
                except Exception, data:
                    print 'error'
'''
def deleteAllData(days = 30):
    d1 = datetime.datetime.now()
    d3 = d1 - datetime.timedelta(days = days)

    objs = Activity.objects.all()
    for item in objs:
        if item.act_time < d3:
            item.delete()
    objs = News.objects.all()
    for item in objs:
        if item.time < d3.date():
            item.delete()
    objs = Lecture.objects.all()
    for item in objs:
        if item.act_time < d3:
            item.delete()

def delNBSP(val = ''):
    strContent = []
    index  = -1;
    for i in range(len(val)):
        strContent.append(val[i])
        if len(strContent) == 0:
            strContent.append(val[i])
            index += 1;
        elif strContent[index] == '>' and val[i] == ' ': 
            pass
        else:
            strContent.append(val[i])
            index += 1
    return ''.join(strContent)

def EnterDisplay(val = ''):
    index =  val.find(':00'.encode('utf-8'))
    i = val.find('<br/>')
    return val[0:i] + '<p></p>' + val[i+5:len(val)]

def LastLineFormat(val = ''):
    flag = True
    index = 0
    lastIndex = 0
    while flag:
        lastIndex = index
        index = val.find('</span>',index + 1)
        if index < 0:
            flag = False
    return val[0:lastIndex + 7]

def endFormat(val = ''):
    end = val.find('<')
    if end == -1:
        end == len(val)
    return val[0:end]

#try:
    getTsinghuaNewsCharacter()
    getTsinghuaNewsSynthesis()
#except:
#   print "error occured in TsinghuaNewsNet"
#try:
    #getArtShowXML()
#except:
    #print "error occured in artshow"
try:
    getStudentTsinghuaNews()
except:
    print "error occured in TsinghuaNews"
'''
try:
    getTsinghuaLecture()
except:
    print "error occured in Lectures"
'''
#deleteAllData()
