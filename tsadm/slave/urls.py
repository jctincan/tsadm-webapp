
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(\d+)/$', 'tsadm.slave.views.dashboard', name='dashboard'),

    url(r'^admin/$', 'tsadm.slave.views.admin', name='admin'),
)
