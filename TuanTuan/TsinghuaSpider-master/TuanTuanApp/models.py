# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import widgets

# Create your models here.
class Activity(models.Model):
    title = models.CharField(_(u'演出名称'),max_length = 255)
    access_time = models.DateField(_(u'爬取时间'), help_text=_(u'此条信息被获取的时间'))
    act_time = models.DateTimeField(_(u'演出时间'),)
    site = models.CharField(_(u'演出地点'), max_length = 255)
    actor = models.CharField(_(u'演出人员'), max_length = 255,blank=True)
    picurl = models.CharField(_(u'图片'), default='http://www.tsinghua.edu.cn/publish/th/campus/trees/view2.jpg', max_length = 100, blank=True, null=True)
    ticket = models.CharField(_(u'票务信息'),max_length = 255,blank=True)
    content = models.TextField(_(u'详细介绍'),max_length = 20000)
    stick = models.SmallIntegerField(_(u'置顶'))
    class Meta:
        verbose_name = _(u'校园演出资讯')
        verbose_name_plural = _(u'校园演出资讯')


class Lecture(models.Model):
    title = models.CharField(_(u'讲座题目'), max_length = 255,unique=True)
    picurl = models.CharField(_(u'图片'), default='http://www.tsinghua.edu.cn/publish/th/campus/trees/view17.jpg',max_length = 100, blank=True, null=True)
    access_time = models.DateField(_(u'爬取时间'), help_text=_(u'此条信息被获取的时间'))
    act_time = models.DateTimeField(_(u'演讲时间'), )
    site = models.CharField(_(u'地点'), max_length = 255)
    actor = models.CharField(_(u'演讲者'), max_length = 255,blank=True)
    content = models.TextField(_(u'详细介绍'), max_length = 20000)
    stick = models.SmallIntegerField(_(u'置顶'))
    class Meta:
        verbose_name = _(u'校园讲座')
        verbose_name_plural = _(u'校园讲座')

class News(models.Model):
    title = models.CharField(_(u'新闻标题'), max_length = 255,unique=True)
    picurl = models.CharField(_(u'图片'), default='http://www.tsinghua.edu.cn/publish/th/campus/trees/view19.jpg', max_length = 100, blank=True, null=True)
    summary = models.CharField(_(u'摘要'), max_length = 255)
    content = models.TextField(_(u'详细内容'), max_length = 20000)
    time = models.DateField(_(u'时间'), )
    stick = models.SmallIntegerField(_(u'置顶'))
    class Meta:
        verbose_name = _(u'校园新闻')
        verbose_name_plural = _(u'校园新闻')

class ModernFigure(models.Model):
    title = models.CharField(_(u'人物标题'), max_length = 255,unique=True)
    picurl = models.CharField(_(u'图片'), max_length = 100, blank=True, null=True)
    content = models.TextField(_(u'详细内容'), max_length = 20000)
    stick = models.SmallIntegerField(_(u'置顶'))
    class Meta:
        verbose_name = _(u'校园人物')
        verbose_name_plural = _(u'校园人物')

class Club(models.Model):
    name = models.CharField(_(u'社团名称'), max_length = 255,unique=True)
    picurl = models.CharField(_(u'图片'), default='http://www.tsinghua.edu.cn/publish/th/campus/trees/view10.jpg',max_length = 100, blank=True, null=True)
    summary = models.CharField(_(u'简要信息'), max_length = 255)
    content = models.TextField(_(u'详细信息'), max_length = 20000)
    stick = models.SmallIntegerField(_(u'置顶'))
    class Meta:
        verbose_name = _(u'社团协会')
        verbose_name_plural = _(u'社团协会')

class Department(models.Model):
    name = models.CharField(_(u'部门名称'), max_length = 255,unique=True)
    picurl = models.CharField(_(u'图片'), default='http://www.tsinghua.edu.cn/publish/th/campus/trees/view17.jpg',max_length = 100, blank=True, null=True)
    summary = models.CharField(_(u'简要信息'), max_length = 255)
    content = models.TextField(_(u'详细信息'), max_length = 20000)
    stick = models.SmallIntegerField(_(u'置顶'))
    class Meta:
        verbose_name = _(u'学校部门')
        verbose_name_plural = _(u'学校部门')





