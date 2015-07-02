# $Id: urls.py 12595 2015-02-11 04:03:44Z jrms $

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'tsadm.user.views.home', name='home'),
    url(r'^admin/$', 'tsadm.user.views.admin', name='admin'),
)
