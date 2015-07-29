
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(\w+)/(\w+)/$', 'tsadm.rsync.views.home', name='home'),
)
