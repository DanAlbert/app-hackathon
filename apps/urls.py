from django.conf.urls.defaults import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('apps.views',
    url(r'^$', 'index'),
    url(r'^about$', 'about'),
    url(r'^rules$', 'rules'),
    url(r'^ideas$', 'ideas'),
    url(r'^submission$', 'submission'),
    
    url(r'^(?P<vote_id>\d+)/vote/$', 'vote'),
)