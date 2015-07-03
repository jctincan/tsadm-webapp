import sys
import os
import os.path
import tempfile
import subprocess
import time

from base64 import b64encode, b64decode

import django
from django.shortcuts import render, redirect

from tsadm.jobq.cmd import TSAdmJobQCmdInvoke, TSAdmJobQCmdNotFound

from tsadm.git.jobq import GIT_CMD_MAP
from tsadm.rsync.jobq import RSYNC_CMD_MAP
from tsadm._mysql.jobq import MYSQL_CMD_MAP
from tsadm.wapp import TSAdmWApp
wapp = TSAdmWApp()


def soft_info(req):
    if not wapp.start(req, '__soft-info', '__soft-info', acclvl='ADMIN'):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()

    tmpl_data['version'] = wapp.version
    tmpl_data['settings'] = wapp.conf

    tmpl_data['django_version'] = django.get_version()
    tmpl_data['python_version'] = '{}.{}.{}'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    tmpl_data['mysql_server_version'] = wapp.db.server_version()
    tmpl_data['mysql_server_charset'] = wapp.db.server_charset()
    tmpl_data['mysql_conn_version'] = wapp.db.conn_version()

    tmpl_data['os_user_uid'] = os.getresuid()
    tmpl_data['os_user_gid'] = os.getresgid()

    tmpl_data['uwsgi_version'] = req.META.get('uwsgi.version', None)

    return render(req, 'soft-info.html', wapp.end(tmpl_data))


def __cmd_args_post_load(POST):
    cmd_args = ''
    for ak, av in POST.items():
        if ak.startswith('tsadm_') and (ak != 'tsadm_cmd' and ak != 'tsadm_return_to'):
            cmd_args = '{} --{}={}'.format(cmd_args, ak.replace('tsadm_', '', 1), av)
    return cmd_args.lstrip()


def cmd_confirm(req):
    if not wapp.start(req, '__cmd_confirm', acclvl='ADMIN_LOW'):
        return wapp.error_page()
    cmd_name = req.POST.get('tsadm_cmd', None)
    if cmd_name is None:
        return wapp.error_page(500, 'no command name')
    return_to = req.POST.get('tsadm_return_to', '/')
    cmd_args = __cmd_args_post_load(req.POST)
    cmd_args_encode = b64encode(cmd_args.encode()).decode()
    tmpl_data = wapp.tmpl_data()
    tmpl_data['return_to'] = return_to
    tmpl_data['cmd'] = {
        'name': cmd_name,
        'args': cmd_args,
        'args_encode': cmd_args_encode,
    }
    return render(req, 'cmd_confirm.html', wapp.end(tmpl_data))


def cmd_exec(req):
    if not wapp.start(req, '__cmd/exec', acclvl='ADMIN_LOW'):
        return wapp.error_page()
    # -- cmd name
    cmd_name = req.POST.get('tsadm_cmd', None)
    if cmd_name is None:
        return wapp.error_page(500, 'no command name')
    # -- cmd args
    cmd_args_encode = req.POST.get('tsadm_cmd_args_encode', None)
    cmd_args = ''
    if cmd_args_encode is not None:
        cmd_args = b64decode(cmd_args_encode.encode())
    # -- cmd map
    cmd_map = dict()
    cmd_map.update(GIT_CMD_MAP)
    cmd_map.update(RSYNC_CMD_MAP)
    cmd_map.update(MYSQL_CMD_MAP)
    # -- exec cmd
    try:
        cmd = TSAdmJobQCmdInvoke(cmd_map, cmd_name, wapp)
    except TSAdmJobQCmdNotFound:
        return wapp.error_page(501, 'command not implemented: '+cmd_name)
    jobq_id = cmd.execute(cmd_args)
    # -- end
    wapp.end()
    return redirect('jobq:info', sname, senv, jobq_id)
