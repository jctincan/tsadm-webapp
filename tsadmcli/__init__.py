import os
__RUN_MODE = 'dev'
os.environ.setdefault('TSADM_MODE', __RUN_MODE)

from tsadm import log
from . import site
from . import siteenv
from . import slave
from . import user

_CMDMAP = {
    'newSite': site.new,
    'siteList': site.list,
    'siteRemove': site.remove,
    'siteEnvList': siteenv.list,
    'newSiteEnv': siteenv.new,
    'siteEnvRemove': siteenv.remove,
    'slaveList': slave.list,
    'newSlave': slave.new,
    'slaveRemove': slave.remove,
    'userList': user.list,
    'newUser': user.new,
    'userRemove': user.remove,
    'userMod': user.modify,
}

def _logOpen(cmd_name):
    log.log_open("tsadm"+__RUN_MODE+"cli")
    log.inf("start: ", cmd_name)
    log.inf("user: ", os.getresuid(), os.getresgid())

def _logClose(status):
    log.inf("end: ", status)
    log.log_close()
    return status

def run(command):
    func = _CMDMAP.get(command, None)
    if func is None:
        raise RuntimeError('invalid command')
    _logOpen(command)
    try:
        rtrn = func()
    except Exception as e:
        print("Exception:", e)
        return _logClose(128)
    else:
        return _logClose(rtrn)
