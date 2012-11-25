from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apps.views',
    url(r'^$', 'projects'),
    url(r'^index$', 'projects'),
    url(r'^projects$', 'projects'),
    url(r'^about$', 'about'),
    url(r'^faq$', 'faq'),
    url(r'^live$', 'live'),
    url(r'^ideas$', 'ideas'),
    
    url(r'^approve/(?P<idea_id>\d+)/$', 'approve'),
    url(r'^project/delete/(?P<proj_id>\d+)/$', 'delete_project'),
    url(r'^idea/delete/(?P<idea_id>\d+)/$', 'delete_idea'),
    url(r'^vote/(?P<vote_id>\d+)/$', 'vote'),
)
