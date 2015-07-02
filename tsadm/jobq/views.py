# $Id: views.py 12365 2015-01-13 04:17:17Z jrms $

from django.shortcuts import render, redirect
from django.http import HttpResponse

import json
import time
import gzip
from base64 import b64decode, b64encode

from tsadm.jobq.cmd import TSAdmJobQCmdInvoke, TSAdmJobQCmdNotFound
from tsadm.jobq.intcmd import TSAdmJobQIntCmdInvoke

from tsadm.git.jobq import GIT_CMD_MAP
from tsadm.rsync.jobq import RSYNC_CMD_MAP
from tsadm._mysql.jobq import MYSQL_CMD_MAP

from tsadm.wapp import TSAdmWApp
wapp = TSAdmWApp()


def get(req, job_id):
    if not wapp.start(req, '__jobq/get', '__jobq/get', acclvl='HOST'):
        return wapp.error_page()

    job_info = wapp.db.jobq_get(job_id)
    wapp.log.dbg('job_info: ', job_info)

    resp_status = 404
    if job_info is not None:
        resp_status = 200

    resp = HttpResponse(json.dumps(job_info), content_type='text/plain; charset=utf-8', status=resp_status)
    wapp.end()
    return resp


def end(req, job_id):
    if not wapp.start(req, '__jobq/end', '__jobq/end', acclvl='HOST'):
        return wapp.error_page()
    wapp.log.dbg('method: ', req.method)

    resp_status = 400
    resp_body = ';-)\n'

    if req.method == 'POST':
        # FIXME: check current status is not END and that job_id exists!!
        cmd_rtrn = req.POST.get('cmd_rtrn', None)
        cmd_out = req.POST.get('cmd_out', None)
        if cmd_rtrn is None or cmd_out is None:
            wapp.log.dbg('jobq.end cmd_rtrn: ', cmd_rtrn)
            wapp.log.dbg('jobq.end cmd_out: ', cmd_out)
            wapp.log.err('jobq.end: bad post data')
            resp_body = ':-(\n'
        else:
            wapp.jobq.end(job_id, cmd_rtrn, cmd_out, compress=False, encode=False)
            resp_status = 200
            resp_body = ':-)\n'
            wapp.log.dbg('jobq.end: done')
    else:
        wapp.log.err('jobq.end: only POSTs allowed')

    resp = HttpResponse(resp_body, content_type='text/plain; charset=utf-8', status=resp_status)
    wapp.end()
    return resp


def info(req, sname, senv, job_id):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()

    job_info = wapp.db.jobq_get_info(wapp.site.env.id, job_id)
    if job_info is None:
        return wapp.error_page(404, 'NO JOB INFO')
    else:
        tmpl_data.update(job_info)
        try:
            tmpl_data['cmd_output'] = gzip.decompress(b64decode(job_info.get('cmd_output', '').encode('utf-8', 'replace'))).decode()
        except Exception as e:
            wapp.log.err('jobq.info: ', e)
            tmpl_data['cmd_output'] = 'INTERNAL ERROR: could not read data'
        tmpl_data['tstamp_start'] = time.strftime(wapp.conf.get('JOB_DATE_FMT'), time.localtime(int(job_info.get('tstamp_start', 0))))

        tse = int(job_info.get('tstamp_end', 0))
        if tse > 0:
            tmpl_data['tstamp_end'] = time.strftime(wapp.conf.get('JOB_DATE_FMT'), time.localtime(tse))
        else:
            tmpl_data['tstamp_end'] = '...'

        tmpl_data['css_class'] = 'error'
        cmd_rtrn = job_info.get('cmd_rtrn', 92)
        wapp.log.dbg('cmd_rtrn: ', cmd_rtrn)

        if cmd_rtrn == 0:
            tmpl_data['css_class'] = 'ok'
        elif cmd_rtrn == 9999:
            tmpl_data['css_class'] = 'start'
        elif cmd_rtrn == 9090:
            tmpl_data['css_class'] = 'run'

    return render(req, 'jobq/info.html', wapp.end(tmpl_data))


def update(req, job_id):
    if not wapp.start(req, '__jobq/update', '__jobq/update', acclvl='HOST'):
        return wapp.error_page()
    wapp.log.dbg('method: ', req.method)

    resp_status = 400
    resp_body = ';-)\n'

    if req.method == 'POST':
        job_status = req.POST.get('job_status', None)
        if job_status is None:
            wapp.log.dbg('jobq.update job_status: ', job_status)
            wapp.log.err('jobq.update: bad post data')
            resp_body = ':-(\n'
        else:
            wapp.jobq.status_update(job_id, job_status)
            resp_status = 200
            resp_body = ':-)\n'
            wapp.log.dbg('jobq.update: ', job_status, ' done')
    else:
        wapp.log.err('jobq.update: only POSTs allowed')

    resp = HttpResponse(resp_body, content_type='text/plain; charset=utf-8', status=resp_status)
    wapp.end()
    return resp


def intcmd_confirm(req, sname, senv, cmd_name):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    tmpl_data = wapp.tmpl_data()
    tmpl_data['cmd'] = {
        'name': cmd_name
    }
    return render(req, 'jobq/intcmd_confirm.html', wapp.end(tmpl_data))


def intcmd_exec(req, sname, senv, cmd_name):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    intcmd = TSAdmJobQIntCmdInvoke(cmd_name, wapp)
    jobq_id = intcmd.execute()
    wapp.end()
    return redirect('jobq:info', sname, senv, jobq_id)


def __cmd_args_post_load(POST):
    cmd_args = ''
    for ak, av in POST.items():
        if ak.startswith('tsadm_') and (ak != 'tsadm_cmd' and ak != 'tsadm_return_to'):
            cmd_args = '{} --{}={}'.format(cmd_args, ak.replace('tsadm_', '', 1), av)
    return cmd_args.lstrip()


def cmd_confirm(req, sname, senv):
    if not wapp.start(req, sname, senv):
        return wapp.error_page()
    cmd_name = req.POST.get('tsadm_cmd', None)
    if cmd_name is None:
        return wapp.error_page(500, 'no command name')
    return_to = req.POST.get('tsadm_return_to', '/return_to-non-set')
    cmd_args = __cmd_args_post_load(req.POST)
    cmd_args_encode = b64encode(cmd_args.encode()).decode()
    tmpl_data = wapp.tmpl_data()
    tmpl_data['return_to'] = return_to
    tmpl_data['cmd'] = {
        'name': cmd_name,
        'args': cmd_args,
        'args_encode': cmd_args_encode,
    }
    return render(req, 'jobq/cmd_confirm.html', wapp.end(tmpl_data))


def cmd_exec(req, sname, senv):
    if not wapp.start(req, sname, senv):
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
