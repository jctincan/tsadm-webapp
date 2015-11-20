import os
os.environ.setdefault('TSADM_MODE', 'dev')

from . import site

def newSite():
    try:
        r = site.new()
    except Exception as e:
        print("Exception:", e)
        return 128
    else:
        return r
