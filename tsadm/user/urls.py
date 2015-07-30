
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'tsadm.user.views.home', name='home'),
    url(r'^admin/$', 'tsadm.user.views.admin', name='admin'),
)
