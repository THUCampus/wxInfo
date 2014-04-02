from django.conf.urls import patterns, include, url
from TuanTuanApp.views import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from TuanTuan import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', entry),
    url(r'^activity/$',activity_page),
    url(r'^lecture/$',lecture_page),
    url(r'^news/$',news_page),
    url(r'^club/$', club_page),
    url(r'^figure/$', figure_page),
    url(r'^department/$', department_page),
    url(r'^admin/', include(admin.site.urls)),
    url(r"^media/(?P<path>.*)$", "django.views.static.serve",{"document_root": settings.MEDIA_ROOT,}),
) + staticfiles_urlpatterns()
