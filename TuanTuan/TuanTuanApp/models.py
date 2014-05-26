# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import widgets
from ckeditor.fields import RichTextField
from TuanTuan.settings import MEDIA_ROOT
from TuanTuan.settings import MEDIA_URL
# Create your models here.

class Activity(models.Model):
    PRIORITY = (
        (0,'0'),
        (1,'1'),
        (2,'2'),
        (3,'3'),
    )
    title = models.CharField(_(u'演出名称'),max_length = 255)
    stick = models.SmallIntegerField(_(u'置顶'),choices=PRIORITY,default=0)
    access_time = models.DateField(_(u'爬取时间'), help_text=_(u'此条信息被获取的时间'))
    act_time = models.DateTimeField(_(u'演出时间'),)
    site = models.CharField(_(u'演出地点'), max_length = 255)
    actor = models.CharField(_(u'演出人员'), max_length = 255,blank=True)
    picurl = models.ImageField(_(u'预览图片'), upload_to="uploads",)
    def PicPreview(self):
        str = self.picurl.name
        if str[0:4] != 'http':
            return '<img src="' + MEDIA_URL + '%s" width="200px"/>' % self.picurl
        else:
            return '<img src="%s" width="200px"/>' % self.picurl
    PicPreview.allow_tags = True
    ticket = models.CharField(_(u'票务信息'),max_length = 255,blank=True)
    content = RichTextField(_(u'详细介绍'),max_length = 20000)
    def __unicode__(self):
        return u'%s' % (self.picurl)
    class Meta:
        verbose_name = _(u'校园演出资讯')
        verbose_name_plural = _(u'校园演出资讯')


class Lecture(models.Model):
    PRIORITY = (
        (0,'0'),
        (1,'1'),
        (2,'2'),
        (3,'3'),
    )
    title = models.CharField(_(u'讲座题目'), max_length = 255,unique=True)
    stick = models.SmallIntegerField(_(u'置顶'),choices=PRIORITY,default=0)
    picurl = models.ImageField(_(u'预览图片'), upload_to="uploads",)
    def PicPreview(self):
        str = self.picurl.name
        if str[0:4] != 'http':
            return '<img src="' + MEDIA_URL + '%s" width="200px"/>' % self.picurl
        else:
            return '<img src="%s" width="200px"/>' % self.picurl
    PicPreview.allow_tags = True
    access_time = models.DateField(_(u'爬取时间'), help_text=_(u'此条信息被获取的时间'))
    act_time = models.DateTimeField(_(u'演讲时间'), )
    site = models.CharField(_(u'地点'), max_length = 255)
    actor = models.CharField(_(u'演讲者'), max_length = 255,blank=True)
    content = RichTextField(_(u'详细介绍'),max_length = 20000)
    def __unicode__(self):
        return u'%s' % (self.picurl)
    class Meta:
        verbose_name = _(u'校园讲座')
        verbose_name_plural = _(u'校园讲座')

class News(models.Model):
    PRIORITY = (
        (0,'0'),
        (1,'1'),
        (2,'2'),
        (3,'3'),
    )
    title = models.CharField(_(u'新闻标题'), max_length = 255,unique=True)
    stick = models.SmallIntegerField(_(u'置顶'),choices=PRIORITY,default=0)
    picurl = models.ImageField(_(u'预览图片'), upload_to="uploads",)
    def PicPreview(self):
        str = self.picurl.name
        if str[0:4] != 'http':
            return '<img src="' + MEDIA_URL + '%s" width="200px"/>' % self.picurl
        else:
            return '<img src="%s" width="200px"/>' % self.picurl
    PicPreview.allow_tags = True
    summary = models.CharField(_(u'摘要'), max_length = 255)
    content = RichTextField(_(u'详细内容2'),max_length = 20000)
    def __unicode__(self):
        return u'%s' % (self.picurl)
    time = models.DateField(_(u'时间'), )
    class Meta:
        verbose_name = _(u'校园新闻')
        verbose_name_plural = _(u'校园新闻')

class ModernFigure(models.Model):
    PRIORITY = (
        (0,'0'),
        (1,'1'),
        (2,'2'),
        (3,'3'),
    )
    title = models.CharField(_(u'就业标题'), max_length = 255,unique=True)
    stick = models.SmallIntegerField(_(u'置顶'),choices=PRIORITY,default=0)
    picurl = models.ImageField(_(u'预览图片'), upload_to="uploads",)
    def PicPreview(self):
        str = self.picurl.name
        if str[0:4] != 'http':
            return '<img src="' + MEDIA_URL + '%s" width="200px"/>' % self.picurl
        else:
            return '<img src="%s" width="200px"/>' % self.picurl
    PicPreview.allow_tags = True 
    content = RichTextField(_(u'详细内容'),max_length = 20000)
    def __unicode__(self):
        return u'%s' % (self.picurl)
    class Meta:
        verbose_name = _(u'就业信息')
        verbose_name_plural = _(u'就业信息')

class Club(models.Model):
    PRIORITY = (
        (0,'0'),
        (1,'1'),
        (2,'2'),
        (3,'3'),
    )
    name = models.CharField(_(u'社团名称'), max_length = 255,unique=True)
    stick = models.SmallIntegerField(_(u'置顶'),choices=PRIORITY,default=0)
    picurl = models.ImageField(_(u'预览图片'), upload_to="uploads",)
    def PicPreview(self):
        str = self.picurl.name
        if str[0:4] != 'http':
            return '<img src="' + MEDIA_URL + '%s" width="200px"/>' % self.picurl
        else:
            return '<img src="%s" width="200px"/>' % self.picurl
    PicPreview.allow_tags = True
    summary = models.CharField(_(u'简要信息'), max_length = 255)
    content = RichTextField(_(u'详细介绍'),max_length = 20000)
    def __unicode__(self):
        return u'%s' % (self.picurl)
    class Meta:
        verbose_name = _(u'社团协会')
        verbose_name_plural = _(u'社团协会')

class Department(models.Model):
    PRIORITY = (
        (0,'0'),
        (1,'1'),
        (2,'2'),
        (3,'3'),
    )
    name = models.CharField(_(u'部门名称'), max_length = 255,unique=True)
    stick = models.SmallIntegerField(_(u'置顶'),choices=PRIORITY,default=0)
    picurl = models.ImageField(_(u'预览图片'), upload_to="uploads",)
    def PicPreview(self):
        str = self.picurl.name
        if str[0:4] != 'http':
            return '<img src="' + MEDIA_URL + '%s" width="200px"/>' % self.picurl
        else:
            return '<img src="%s" width="200px"/>' % self.picurl
    PicPreview.allow_tags = True
    summary = models.CharField(_(u'简要信息'), max_length = 255)
    content = RichTextField(_(u'详细介绍'),max_length = 20000)
    def __unicode__(self):
        return u'%s' % (self.picurl)
    class Meta:
        verbose_name = _(u'学校部门')
        verbose_name_plural = _(u'学校部门')





