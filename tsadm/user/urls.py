
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'tsadm.user.views.home', name='home'),

    url(r'^addkey/$', 'tsadm.user.views.addkey', name='addkey'),
    url(r'^showkey/([a-zA-Z0-9:]+)/$', 'tsadm.user.views.showkey', name='showkey'),
    url(r'^delkey/([a-zA-Z0-9:]+)/$', 'tsadm.user.views.delkey', name='delkey'),

    url(r'^admin/$', 'tsadm.user.views.admin', name='admin'),
)
