import os
__RUN_MODE = 'dev'
os.environ.setdefault('TSADM_MODE', __RUN_MODE)


from tsadm import log
from . import site


def _logOpen(cmd_name):
    log.log_open("tsadm"+__RUN_MODE+"cli")
    log.inf("start: ", cmd_name)
    log.inf("user: ", os.getresuid(), os.getresgid())


def _logClose(status):
    log.inf("end: ", status)
    log.log_close()


def newSite():
    _logOpen("newSite")
    try:
        r = site.new()
    except Exception as e:
        print("Exception:", e)
        _logClose(128)
        return 128
    else:
        _logClose(r)
        return r
