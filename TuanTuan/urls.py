from django.conf.urls import patterns, include, url
from django.shortcuts import redirect
from TuanTuanApp.views import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from TuanTuan import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', redirect('http://student.tsinghua.edu.cn')),
    url(r'^activity/$',activity_page),
    url(r'^lecture/$',lecture_page),
    url(r'^news/$',news_page),
    url(r'^club/$', club_page),
    url(r'^figure/$', figure_page),
    url(r'^department/$', department_page),
    url(r'^admin/', include(admin.site.urls)),
    url(r"^media/(?P<path>.*)$", "django.views.static.serve",{"document_root": settings.MEDIA_ROOT,}),
    url(r'^ckeditor/', include('ckeditor.urls')),
) + staticfiles_urlpatterns()
