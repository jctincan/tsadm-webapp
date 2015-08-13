import os
import syslog as sl

from . import config


def log_open(iden='tsadmdev'):
    sl.openlog(iden, sl.LOG_PID, sl.LOG_LOCAL3)


def log_close():
    sl.closelog()


def dbg(*msg):
    __log(sl.LOG_DEBUG, 'DBG: ', *msg)


def inf(*msg):
    __log(sl.LOG_DEBUG, 'INF: ', *msg)


def err(*msg):
    __log(sl.LOG_DEBUG, 'ERR: ', *msg)


def wrn(*msg):
    __log(sl.LOG_DEBUG, 'WRN: ', *msg)


def __log(prio, *msg):
    line = ''
    for m in msg:
        if type(m) == type(''):
            line += m
        else:
            line += str(m)
    sl.syslog(prio, line)
