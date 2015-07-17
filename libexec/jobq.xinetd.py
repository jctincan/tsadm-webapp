#!/usr/bin/env python3

import sys
import re
import os
import os.path
import subprocess

BASE_DIR = '/opt/tsadmdev'
sys.path.insert(0, os.path.join(BASE_DIR, 'libexec'))
sys.path.insert(0, BASE_DIR)

import tsadm.config as tsadm_conf
import tsadm.log
import runner


at_cmd = '/usr/bin/at'
runbg_cmd = os.path.join(BASE_DIR, 'libexec', 'jobq.runbg.py')
re_job_id = re.compile(r'^[a-f0-9]+$')

resp_headers = {
    'ERROR': '500 INTERNAL ERROR\n',
    'BADREQ': '400 BAD REQUEST\n',
    'BADCMD': '401 BAD COMMAND\n',
    'NOTCMD': '402 COMMAND NOT FOUND\n',
    'BADJID': '403 BAD JOB ID\n',
    'NOSITE': '404 SITE NOT FOUND\n',
    'OK': '200 OK'
}


def _exit(status):
    tsadm.log.dbg('END')
    tsadm.log.log_close()
    sys.exit(status)


def _exit_badreq(req_line):
    tsadm.log.err('bad request: ', req_line)
    print(resp_headers['BADREQ'])
    _exit(1)


# --- start log
tsadm.log.log_open(tsadm_conf.get('JOBQ_SYSLOG_TAG', 'tsadmdev-jobqd'))
tsadm.log.dbg('START')
tsadm.log.dbg('sys.path: ', sys.path)
tsadm.log.dbg('os.environ: ', os.environ)

# --- read request
req_line = sys.stdin.readline().strip()
tsadm.log.dbg('req_line: ', req_line)

line_items = req_line.split(' ')
try:
    req = line_items[0]
    req_args = line_items[1:]
except IndexError:
    tsadm.log.dbg('bad args')
    _exit_badreq(req_line)

tsadm.log.dbg('req: ', req)
tsadm.log.dbg('req_args: ', req_args)

# --- check request
if req != '.run' and req != '.runbg' or len(req_args) < 1:
    _exit_badreq(req_line)

# --- run requested job
if req == '.run':

    # -- get args
    try:
        sname = req_args[0]
        senv = req_args[1]
        cmd_name = req_args[2]
    except IndexError:
        _exit_badreq(req_line)

    try:
        cmd_args = req_args[3:]
    except:
        cmd_args = []

    # -- cd to site's env home
    if not runner.chdir(sname, senv):
        print(resp_headers['NOSITE'])
        _exit(1)

    # -- check cmd name
    if not runner.check_cmd_name(cmd_name):
        print(resp_headers['BADCMD'])
        _exit(1)

    # -- check cmd path
    cmd_path = runner.cmd_path(BASE_DIR, cmd_name)
    if cmd_path is None:
        print(resp_headers['BADCMD'])
        _exit(1)

    # -- run command
    cmd_rtrn, cmd_out = runner.run(cmd_path, cmd_args)
    tsadm.log.dbg('cmd_rtrn: ', cmd_rtrn)

    print(resp_headers['OK'])
    print('CMD-RTRN:', cmd_rtrn)
    print()

    if cmd_out is None:
        tsadm.log.wrn('cmd_name: ', cmd_name, ' - cmd_out: ', cmd_out)
    else:
        for l in cmd_out.readlines():
            print(l.decode('utf-8', 'replace'), end='')
        cmd_out.close()

    tsadm.log.inf('{}:{}'.format(cmd_name, cmd_rtrn))
    _exit(0)

elif req == '.runbg':

    if not os.path.exists(at_cmd) or not os.access(at_cmd, os.X_OK):
        tsadm.log.err(at_cmd, ': not found or executable')
        print(resp_headers['ERROR'])
        _exit(1)

    if not os.path.exists(runbg_cmd) or not os.access(runbg_cmd, os.X_OK):
        tsadm.log.err(runbg_cmd, ': not found or executable')
        print(resp_headers['ERROR'])
        _exit(1)

    job_id = req_args[0]
    if not re_job_id.match(job_id):
        tsadm.log.err('bad jobid: ', job_id)
        print(resp_headers['BADJID'])
        _exit(1)

    at_input = '{} --job-id={}'.format(runbg_cmd, job_id)
    at = subprocess.Popen([at_cmd, 'now'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        at_out, at_err = at.communicate(at_input.encode('utf-8', 'replace'))
        at_rtrn = at.wait()
        at_out = at_out.decode('utf-8', 'replace').replace('warning: commands will be executed using /bin/sh', '')
    except subprocess.TimeoutExpired as e:
        tsdam.log.err('at comm: ', e)
        at_out = 'at comm failed'
        at_rtrn = 128

    print(resp_headers['OK'])
    print('CMD-RTRN:', at_rtrn)
    print()
    print('START:', job_id, sep='')
    print(at_out)
    tsadm.log.inf('{}[{}]: runbg'.format(job_id, at_rtrn))
    _exit(0)

tsadm.log.err('end of program reached!')
print(resp_headers['ERROR'])
_exit(128)
