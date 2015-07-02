# $Id: urls.py 11585 2014-07-31 03:12:19Z jrms $

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(\w+)/(\w+)/$', 'tsadm.help.views.site', name='site'),
)
