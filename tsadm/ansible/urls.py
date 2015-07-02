# $Id: urls.py 12772 2015-04-10 19:26:34Z jrms $

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^inv/lst/$', 'tsadm.ansible.views.invlist', name='invlist'),
)
