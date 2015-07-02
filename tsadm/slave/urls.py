# $Id: urls.py 12294 2014-12-11 04:16:49Z jrms $

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(\d+)/$', 'tsadm.slave.views.dashboard', name='dashboard'),

    url(r'^admin/$', 'tsadm.slave.views.admin', name='admin'),
)
