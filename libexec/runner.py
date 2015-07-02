#!/usr/bin/env python3
# $Id: runner.py 12754 2015-04-07 03:55:08Z jrms $

import subprocess
import tempfile
import re
import os
import os.path

from tsadm.settings import TSADM as tsadm_conf
import tsadm.log

sites_home_base = tsadm_conf.get('SITE_HOME_BASE', '/home/tsadm/sites')
re_cmd_name = re.compile(r'^[a-z0-9\.-]+$')


def __args2env(args):
    e = dict()
    for a in args:
        ai = a.split('=')
        ek = ai[0].replace('--', '', 1).upper()
        ev = '='.join(ai[1:])
        e[ek] = ev
    return e


def run(cmd_path, cmd_args):
    # NOTE: child process stderr MUST be the same as stdout, as some
    #       commands (git mostly), show useful information (not only
    #       when they fail) on stderr.
    tsadm.log.dbg('start run: ', cmd_path, ' ', cmd_args)
    tsadm.log.dbg('runner environ: ', os.environ)
    cmd_env = __args2env(cmd_args)
    cmd_env['PATH'] = '/usr/bin:/bin'
    cmd_env['PYTHONIOENCODING'] = tsadm_conf.get('CHARSET', 'utf-8')
    tsadm.log.dbg('cmd_env: ', cmd_env)
    cmd_out = None
    cmd_rtrn = None
    try:
        cmd_out = tempfile.TemporaryFile()
    except Exception as e:
        tsadm.log.err('run: ', e)
        return (64, None)
    tsadm.log.dbg('cmd_out: ', cmd_out)
    try:
        tsadm.log.dbg('run: ', cmd_path, ' ', cmd_env)
        cmd_rtrn = subprocess.call([cmd_path], env=cmd_env, stdout=cmd_out, stderr=cmd_out)
    except Exception as e:
        tsadm.log.dbg('runing: ', e)
        tsadm.log.err('runing: ', cmd_path, ' ', cmd_env)
    if cmd_rtrn is None:
        cmd_rtrn = 128
    cmd_out.seek(0, 0)
    return (cmd_rtrn, cmd_out)


def check_cmd_name(cmd_name):
    if not re_cmd_name.match(cmd_name):
        tsadm.log.err('bad cmd: ', cmd_name)
        return False
    return True


def cmd_path(base_dir, cmd_name):
    libexec = os.path.realpath(base_dir + '/libexec/jobq')
    cmd_path = '/'.join([libexec, re.sub(r'\.', '/', cmd_name)])
    tsadm.log.dbg('cmd_path: ', cmd_path)

    if not os.path.exists(cmd_path) or not os.access(cmd_path, os.X_OK):
        tsadm.log.err('not cmd: ', cmd_path)
        return None

    cmd_realpath = os.path.realpath(cmd_path)
    tsadm.log.dbg('cmd_realpath: ', cmd_realpath)

    if not cmd_realpath.startswith(libexec):
        tsadm.log.err('bad cmd path: ', cmd_realpath)
        return None

    return cmd_realpath


def chdir(sname, senv):
    cdir_to = '/tmp'
    if not sname.startswith('__slave/'):
        senv_home = os.path.join(sites_home_base, sname, senv)
        if os.access(senv_home, os.F_OK | os.R_OK | os.X_OK):
            cdir_to = senv_home
        else:
            tsadm.log.dbg('os.uid: ', os.getuid())
            tsadm.log.dbg('os.gid: ', os.getgid())
            tsadm.log.err('no site: ', senv_home)
            return False
    os.chdir(cdir_to)
    return True
