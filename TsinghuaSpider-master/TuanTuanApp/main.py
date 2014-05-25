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
import datetime
def getArtShowXML():
    print "hehe"
    url = 'http://www.hall.tsinghua.edu.cn/column/pwzx_hdap'
    rootUrl = 'http://www.hall.tsinghua.edu.cn'
    content = urllib2.urlopen(url).read()
    soup = bs4.BeautifulSoup(content)
    #find all <a> links
    mytable = soup.find_all("ul", class_="hd_list")
    #server to post
    #server = 'http://tuantuan.ssast.org/sql/activity/'

    #from 9th to 24th
    for item in mytable:
        title = item.a.text
        link = item.a['href']
        ticket=item.li.text

        #search for id
        #regex = re.search("[0-9]+", link)
        #number = string.atoi(regex.group(0))
        content = urllib2.urlopen('http://www.hall.tsinghua.edu.cn/' + link).read()
        root = bs4.BeautifulSoup(content)
        #contents in the 5th table
        table = root.html.find_all("div", class_="column_1")[0]
        picurl = rootUrl + table.img['src']
        imgs = table.findAll('img')
        imgs[0].extract()
        imgs.remove(imgs[0])

        for img in imgs:
            img.parent['style'] = 'line-height: 125%; text-align: center;'
            if img['src'][len(img['src'])-3: len(img['src'])] != 'gif':
                img['style'] = "width:95%; border-radius: 8px; text-align: center;"
                img['height'] = ""
                img['width'] = ""
            if img['src'][0:4] != 'http':
                img['src'] = rootUrl + img['src']
        pTags = table.findAll('p')
        for p in pTags:
            p['style'] = "line-height:25px;"
	#table.img['src'] = 'http://www.hall.tsinghua.edu.cn' + table.img['src']
        acttitle = table.find_all("div", class_="xqy_p")[0].find_all("p")[1].text

        try:
            curtime = table.find_all("li", class_="time_1")[0].text.encode("utf-8")
            curtime =curtime.replace("年", "-")
            curtime = curtime.replace("月", "-")
            curtime = curtime.replace("日", " ")
            dates = []
            daystr = curtime.split(' ')[0]
            daystr = daystr.split(',')
            for dateitem in daystr:
                date = dateitem.split("-")
                year = date[0]
                month = date[1]
                days = date[2].split(" ")[0].split("/")
                for item in days:
                    dates.append(year+"-"+month+"-"+item);
            timeloc = curtime.find(":")
            time = curtime[timeloc-2:timeloc+3]

            timearray = []
            for item in dates:
                timearray.append(item + " "+time)
            site=table.find_all("li", class_="add")[0].text
            val=table


            access_time = "1993-01-01"
            #print title.encode('utf-8')
            #print picurl
            #print access_time
            #print "\n"
	    #print curtime.encode('utf-8')
            #print site.encode('utf-8')
            #print  ticket.encode('utf-8')
	    print val
            for item in timearray:
                activity = Activity.objects.filter(title=title, act_time=item)
                if activity.count() == 0:
                  Activity.objects.create(title=title, picurl=picurl, access_time=access_time, act_time=item, site=site,
                        actor='', ticket=ticket, content = val, stick = 0)
        except Exception, data:
            continue

def getTsinghuaCareerCenter():
    rootUrl = 'http://career.tsinghua.edu.cn'
    urls = 'http://career.tsinghua.edu.cn/publish/career/8130/index.html'
    indexPage = urllib2.urlopen(urls)
    indexContent = indexPage.read()
    indexRoot = bs4.BeautifulSoup(indexContent)
    linklist = indexRoot.find('div', {"class": "chapter1"}).ul.findAll('li')
	iter = 0
	picurls = ['http://careertipsinfo.com/wp-content/uploads/2009/12/Career-Changes.jpg', 
			'http://news.xd56b.com/gtsc/20110912/SC0912-A3_1.jpg', 
			'http://img.taopic.com/uploads/allimg/130725/318765-130H5091R696.jpg',
			'http://www.albiz.cn:88/imgMsg88/201312/20131221085222784.jpg',
			'http://www.ganqi.com/Images/KE/image/20120510/20120510085316_78015.jpg',
			'http://img.article.pchome.net/00/40/94/87/pic_lib/s960x639/office_3006s960x639.jpg',
			'http://www.bkoa.cn/uFile/2849/20112229935318.jpg',
			'http://wp1.sina.cn/woriginal/70f7d973jw1e3ahp0pgetj.jpg',
			'http://www.yan168.com/uploadfiles/pic/20100813131115416A.jpg',
			'http://imgs.ebrun.com/resources/2011_06/2011_06_30/201106304571309398970171.jpg']
    for item in linklist:
        #title
		picurl = picurls[iter%len(picurls)]
        title = item.p.a.contents[0]
        if(title[0:4] == u'[置顶]'):
            stick = 1
            title = title[4:len(title)]
        else:
            stick = 0
        title = title.encode('utf-8')
        tmpUrl = item.p.a['href']
        page = urllib2.urlopen(rootUrl + tmpUrl)
        content = page.read()
        root = bs4.BeautifulSoup(content)
        #content
        htmlText = root.find('div', {"class" : "chapter"})

        imgs = htmlText.findAll('img')
        for item in imgs:
            l = len(item['src'])
            if(item['src'][l-4:l] == ".gif"):
                continue
            if item['src'][0:4] != 'http':
                picurl = rootUrl + item['src']
                break
            else:
                picurl =  item['src']
                break

        content = str(htmlText)
        cr = ModernFigure.objects.filter(title=title)
        if len(cr) == 0:
            try:
                ModernFigure.objects.create(title=title, content=content, picurl=picurl, stick=stick)
                print title
            except Exception, data:
                print "error"

def getTsinghuaNewsCharacter():
    rootUrl = 'http://news.tsinghua.edu.cn'
    urls = 'http://news.tsinghua.edu.cn/publish/news/4208/index.html'
    print "world"
    indexPage = urllib2.urlopen(urls)
    print "hello"
    indexContent = indexPage.read()
    print "hhe"
    indexRoot = bs4.BeautifulSoup(indexContent)
    linklist = indexRoot.find('div', id = 'datalist_sec2').ul.findAll('li')
    for item in linklist:
        #title
        title = item.a.string.encode('utf-8')
        picurl = ''
        tmpUrl = item.a['href']
        page = urllib2.urlopen(rootUrl + tmpUrl)
        print "subhello"
        content = page.read()
        root = bs4.BeautifulSoup(content)
        #content
        htmlText = root.find('div', id = 'datalist_detail')

        pTags = htmlText.findAll('p')
        for p in pTags:
            p['style'] += "line-height:25px;"
        #img
        imgs = htmlText.findAll('img')
        for item in imgs:
            l = len(item['src'])
            if(item['src'][l-4:l] == ".gif"):
                continue
            if item['src'][0:4] != 'http':
                picurl = rootUrl + item['src']
                break
            else:
                picurl =  item['src']
                break
            print picurl
        for img in imgs:
            img.parent['style'] = 'line-height: 125%; text-align: center;'
            if img['src'][len(img['src'])-3: len(img['src'])] != 'gif':
                img['style'] = "width:95%; border-radius: 8px; text-align: center;"
                img['height'] = ""
                img['width'] = ""
            if img['src'][0:4] != 'http':
                img['src'] = rootUrl + img['src']
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


        pTags = htmlText.findAll('p')
        for p in pTags:
            p['style'] += "line-height:25px;"
        #img
        imgs = htmlText.findAll('img')
        for item in imgs:
            l = len(item['src'])
            if(item['src'][l-4:l] == ".gif"):
                continue
            if item['src'][0:4] != 'http':
                picurl = rootUrl + item['src']
                break
            else:
                picurl =  item['src']
                break
            print picurl

        for img in imgs:
            img.parent['style'] = 'line-height: 125%; text-align: center;'
            if img['src'][len(img['src'])-3: len(img['src'])] != 'gif':
                img['style'] = "width:95%; border-radius: 8px; text-align: center;"
                img['height'] = ""
                img['width'] = ""
            if img['src'][0:4] != 'http':
                img['src'] = rootUrl + img['src']
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
    #print "time"
    d3 = d1 - datetime.timedelta(days = 20)
    url1 = 'http://166.111.17.5:8080/getNews?'
    urlparam = {
        'start_time':d3.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time':d1.strftime('%Y-%m-%d %H:%M:%S'),
        'valid_code':'tuanwei'
    }
    print url1
    sd = urllib.urlencode(urlparam)
    url2 = url1 + sd
    print url2
    page = urllib2.urlopen(url2)
    print url2
    #page = urllib2.urlopen('''http://166.111.17.5:8080/getNews?start_time=2013-11-10%2000:00:00&end_time=2013-12-21%2000:00:00&valid_code=tuanwei''')
    content = page.read()
    json_read = json.loads(content)
    print content
    if(json_read['result'] == 'success'):

        for item in json_read['news']:
            title = item['title'].encode('utf-8')
            print title
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
#    getTsinghuaNewsCharacter()
#    getTsinghuaNewsSynthesis()
#except:
#   print "error occured in TsinghuaNewsNet"
try:
    getArtShowXML()
except:
    print "error occured in artshow"
    
try:
    getTsinghuaCareerCenter()
except:
    print "error occured in career"
    
try:
    getStudentTsinghuaNews()
    getTsinghuaNewsCharacter()
    getTsinghuaNewsSynthesis()
except:
    print "error occured in TsinghuaNewsNet"
#try:
    #i = 0
#getArtShowXML()
#except:
 #   print "error occured in artshow"
try:
    i = 0
    #getStudentTsinghuaNews()
except:
    print "error occured in TsinghuaNews"
'''
try:
    getTsinghuaLecture()
except:
    print "error occured in Lectures"
'''
