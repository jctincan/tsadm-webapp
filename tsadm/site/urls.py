
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^admin/$', 'tsadm.site.views.admin', name='admin'),

    url(r'^index/$', 'tsadm.site.views.index', name='index'),
    url(r'^(\w+)/(\w+)/$', 'tsadm.site.views.dashboard', name='dashboard'),

    url(r'^(\w+)/(\w+)/log/$', 'tsadm.site.views.log', name='log'),

    url(r'^(\w+)/(\w+)/lock/$', 'tsadm.site.views.lock_confirm', name='lock_confirm'),
    url(r'^(\w+)/(\w+)/lock/([a-f0-9]+)/$', 'tsadm.site.views.lock', name='lock'),

    url(r'^(\w+)/(\w+)/unlock/$', 'tsadm.site.views.unlock_confirm', name='unlock_confirm'),
    url(r'^(\w+)/(\w+)/unlock/([a-f0-9]+)/$', 'tsadm.site.views.unlock', name='unlock'),

    url(r'^(\w+)/(\w+)/claim/$', 'tsadm.site.views.claim_confirm', name='claim_confirm'),
    url(r'^(\w+)/(\w+)/claim/([a-f0-9]+)/$', 'tsadm.site.views.claim', name='claim'),

    url(r'^(\w+)/(\w+)/release/$', 'tsadm.site.views.release_confirm', name='release_confirm'),
    url(r'^(\w+)/(\w+)/release/([a-f0-9]+)/$', 'tsadm.site.views.release', name='release'),

    url(r'^envRedir/$', 'tsadm.site.views.env_redir', name='envRedir'),
)
