import os
os.environ.setdefault('TSADM_MODE', 'dev')

from . import site

def newSite():
    return site.new()
