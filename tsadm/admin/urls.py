
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'tsadm.admin.views.home', name='home'),
    url(r'^activity/$', 'tsadm.admin.views.activity', name='activity'),
    url(r'^activity/(\d+)/$', 'tsadm.admin.views.activity', name='activity'),
    url(r'^dbmaint/$', 'tsadm.admin.views.dbmaint', name='dbmaint'),
)
