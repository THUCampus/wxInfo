__author__ = 'Allen'

from django.contrib import admin
from models import Activity, Lecture, News,Club, Department, ModernFigure
from django.forms import TextInput, Textarea
from django.db import models
from django import forms

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'act_time', 'site','stick','PicPreview')
    list_filter = ('act_time',)
    ordering = ('-stick', '-act_time',)
    search_fields = ('title',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 15, 'cols': 100})},
        models.CharField: {'widget': Textarea(attrs={'rows': 1, 'cols': 100})},
    }


admin.site.register(Activity, ActivityAdmin)

class EmployAdmin(admin.ModelAdmin):
    list_display = ('title', 'stick','PicPreview')
    list_filter = ('id',)
    ordering = ('-id',)
    search_fields = ('title',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 15, 'cols': 100})},
        models.CharField: {'widget': Textarea(attrs={'rows': 1, 'cols': 100})},
    }


admin.site.register(ModernFigure, EmployAdmin)


class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'act_time', 'actor', 'site','stick','PicPreview')
    list_filter = ('act_time',)
    ordering = ('-stick','-act_time',)
    search_fields = ('title', 'actor',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 15, 'cols': 100})},
        models.CharField: {'widget': Textarea(attrs={'rows': 1, 'cols': 100})},
    }

admin.site.register(Lecture, LectureAdmin)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'time', 'summary','stick','PicPreview')
    list_filter = ('time',)
    ordering = ('-stick','-time',)
    search_fields = ('title','summary')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 15, 'cols': 100})},
        models.CharField: {'widget': Textarea(attrs={'rows': 1, 'cols': 100})},
    }

admin.site.register(News, NewsAdmin)

class ClubAdmin(admin.ModelAdmin):
    list_display = ('name','summary','stick','PicPreview')
    search_fields = ('name','summary',)
    ordering = ('-stick',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 15, 'cols': 100})},
        models.CharField: {'widget': Textarea(attrs={'rows': 1, 'cols': 100})},
    }

admin.site.register(Club, ClubAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name','summary','stick','PicPreview')
    search_fields = ('name','summary')
    ordering = ('-stick',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 15, 'cols': 100})},
        models.CharField: {'widget': Textarea(attrs={'rows': 1, 'cols': 100})},
    }

admin.site.register(Department, DepartmentAdmin)
