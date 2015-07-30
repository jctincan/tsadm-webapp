
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(\w+)/(\w+)/$', 'tsadm._mysql.views.home', name='home'),
)
