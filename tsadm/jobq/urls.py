# $Id: urls.py 12180 2014-11-29 06:09:59Z jrms $

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^get/([a-f0-9]+)/$', 'tsadm.jobq.views.get', name='get'),
    url(r'^end/([a-f0-9]+)/$', 'tsadm.jobq.views.end', name='end'),
    url(r'^update/([a-f0-9]+)/$', 'tsadm.jobq.views.update', name='update'),

    url(r'^(\w+)/(\w+)/info/([a-f0-9]+)/$', 'tsadm.jobq.views.info', name='info'),

    url(r'^icc/(\w+)/(\w+)/([\w.-]+)/$', 'tsadm.jobq.views.intcmd_confirm', name='intcmd_confirm'),
    url(r'^ice/(\w+)/(\w+)/([\w.-]+)/$', 'tsadm.jobq.views.intcmd_exec', name='intcmd_exec'),

    url(r'^cc/(\w+)/(\w+)/$', 'tsadm.jobq.views.cmd_confirm', name='cmd_confirm'),
    url(r'^ce/(\w+)/(\w+)/$', 'tsadm.jobq.views.cmd_exec', name='cmd_exec'),
)
