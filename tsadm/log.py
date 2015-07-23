import os
import sys
import syslog as sl

from . import config


class __G:
    devmode = False


if config.get('RUN_MODE', '') == 'dev':
    __G.devmode = True


def log_open(iden='tsadmdev'):
    sl.openlog(iden, sl.LOG_PID, sl.LOG_LOCAL3)


def log_close():
    sl.closelog()


def dbg(*msg):
    __log(sl.LOG_DEBUG, 'DBG: ', *msg)


def inf(*msg):
    __log(sl.LOG_NOTICE, 'INF: ', *msg)


def err(*msg):
    __log(sl.LOG_ERR, 'ERR: ', *msg)


def wrn(*msg):
    __log(sl.LOG_WARNING, 'WRN: ', *msg)


def __log(prio, *msg):
    line = ''
    for m in msg:
        if type(m) == type(''):
            line += m
        else:
            line += str(m)
    if __G.devmode:
        print(line, file=sys.stderr)
    sl.syslog(prio, line)
