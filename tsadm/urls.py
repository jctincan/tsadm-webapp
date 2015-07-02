# $Id: urls.py 12762 2015-04-07 22:25:30Z jrms $

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'tsadm.site.views.index', name='index'),
    url(r'^soft-info/$', 'tsadm.views.soft_info', name='soft-info'),

    url(r'^cmd/confirm/$', 'tsadm.views.cmd_confirm', name='cmd_confirm'),
    url(r'^cmd/exec/$', 'tsadm.views.cmd_exec', name='cmd_exec'),

    url(r'^admin/', include('tsadm.admin.urls', namespace='admin')),
    url(r'^site/', include('tsadm.site.urls', namespace='site')),
    url(r'^git/', include('tsadm.git.urls', namespace='git')),
    url(r'^files/', include('tsadm.rsync.urls', namespace='rsync')),
    url(r'^db/', include('tsadm._mysql.urls', namespace='mysql')),
    url(r'^jobq/', include('tsadm.jobq.urls', namespace='jobq')),
    url(r'^help/', include('tsadm.help.urls', namespace='help')),
    url(r'^user/', include('tsadm.user.urls', namespace='user')),
    url(r'^slave/', include('tsadm.slave.urls', namespace='slave')),
    url(r'^asb/', include('tsadm.ansible.urls', namespace='ansible')),
)
