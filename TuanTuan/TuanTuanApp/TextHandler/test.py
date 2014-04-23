# -*- coding: utf-8 -*-
from TuanTuan.TuanTuanApp.TextHandler.entry import TextProcess
from datetime import datetime

while True:
    text = raw_input()
    if text == 'Q' or text == 'q':
        break
    start = datetime.now()
    pro = TextProcess(inputText=text.decode('gbk'), tags=[])
    results = pro.process()
    end = datetime.now()
    for result in results:
        print "result name = " + result['name']
        print "mark = " + str(result['mark'])
        for each in result['data']:
            try:
                print "item = " + each.name
            except:
                try:
                    print "item = " + each.title
                except:
                    print "item = 无法输出的条目"
    print end - start

