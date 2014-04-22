# -*- coding: utf-8 -*-
import urllib
import urllib2
import json

def access_token():
    #response = urllib2.urlopen('''https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxba2385bd8746d139&secret=0c1108bc87c5068ed94703c19038cb03''')
    global access_token
    access_token = 't7-jhsJYGx6lzv_m_OQttGo66uK5U8u5j9bxJLSdSu8Mk3xzs870egg5TaR99plXHARtzW2IwKHc2P9vwg-VDM3KY4KJTRRXkYbJiavCM-Z5ojv9HHu4JA0Q6byq53Ww66rU4zBzJm9a1Hp2zdkiRg'
    #access_token = json.loads(response.read())['access_token']
    global test
    test = 'access_token'
    return access_token

def send_msg(OpenID, type = 'text'):
    if type == 'text':
        data = {"touser": OpenID,"msgtype": "text","text":{"content": "Hello World"}}
    elif type == 'news':
        data = {
            "touser":OpenID,
            "msgtype":"news",
            "news":{
                "articles": [
                    {
                        "title":'梁山伯与祝英台',
                        "description":'''剧目：“幽兰雅韵”清华大学2013昆曲文化艺术周——江苏省演艺集团昆剧院《梁山伯与祝英台》\n时间：2013-12-2 19:30:00\n地点：新清华学堂\n演出：江苏省演艺集团昆剧院\n票价：20售罄/40/60/100/150/200元/VIP\n售票状态：售票中\n''',
                        "url":'http://www.hall.tsinghua.edu.cn/ycshow.aspx?id=323',
                        "picurl":'http://115.28.161.192/TuanTuan/images/large_5C0n_19af0001bf141260.jpg'
                    }
                ]
            }
        }
    url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + access_token
    data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    re = urllib2.urlopen(req)
    return

