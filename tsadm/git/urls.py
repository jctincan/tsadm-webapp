
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(\w+)/(\w+)/$', 'tsadm.git.views.home', name='home'),
    url(r'^hook/post-receive/$', 'tsadm.git.views.post_receive', name='post_receive'),
)
