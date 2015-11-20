import os
__RUN_MODE = 'dev'
os.environ.setdefault('TSADM_MODE', __RUN_MODE)


from tsadm import log
from . import site


def _logOpen(cmd_name):
    log.log_open("tsadm"+__RUN_MODE+"cli")
    log.inf("start")
    log.inf("user: ", os.getresuid(), os.getresgid())
    log.inf("command: ", cmd_name)


def _logClose():
    log.inf("end")
    log.log_close()


def newSite():
    _logOpen("newSite")
    try:
        r = site.new()
    except Exception as e:
        print("Exception:", e)
        _logClose()
        return 128
    else:
        _logClose()
        return r
