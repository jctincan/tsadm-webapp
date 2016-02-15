import os
__RUN_MODE = 'dev'
os.environ.setdefault('TSADM_MODE', __RUN_MODE)

from tsadm import log
from . import site
from . import siteenv

_CMDMAP = {
    'newSite': site.new,
    'siteList': site.list,
    'siteRemove': site.remove,
    'siteEnvList': siteenv.list,
    'newSiteEnv': siteenv.new,
    'siteEnvRemove': siteenv.remove,
}

def _logOpen(cmd_name):
    log.log_open("tsadm"+__RUN_MODE+"cli")
    log.inf("start: ", cmd_name)
    log.inf("user: ", os.getresuid(), os.getresgid())

def _logClose(status):
    log.inf("end: ", status)
    log.log_close()

def run(command):
    func = _CMDMAP.get(command, None)
    if func is None:
        raise RuntimeError('invalid command')
    _logOpen(command)
    try:
        rtrn = func()
    except Exception as e:
        print("Exception:", e)
        _logClose(128)
        return 128
    else:
        _logClose(rtrn)
        return rtrn
