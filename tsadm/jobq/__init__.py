# $Id: __init__.py 12179 2014-11-29 05:55:57Z jrms $

import hashlib
import time
import telnetlib
import os
import gzip

from base64 import b64encode

import tsadm.log


class TSAdmJobQ:
    _db = None
    _user_id = None
    _senv_id = None
    _site_name = None
    _site_env = None
    _conf = None
    _cmd_hooks = None
    _server_addr = None


    def __init__(self, db, user_id, senv_id, sname, senv, conf):
        self._db = db
        self._user_id = user_id
        self._senv_id = senv_id
        self._site_name = sname
        self._site_env = senv
        self._conf = conf
        self._cmd_hooks = dict()


    def idgen(self):
        d = hashlib.sha1()
        d.update(str(time.time()).encode('utf-8', 'replace'))
        d.update(str(self._user_id).encode('utf-8', 'replace'))
        d.update(str(self._senv_id).encode('utf-8', 'replace'))
        d.update(self._site_name.encode('utf-8', 'replace'))
        d.update(self._site_env.encode('utf-8', 'replace'))
        hd = d.hexdigest()
        del d
        return hd


    def start(self, cmd_name, cmd_args, senv_id=None, adm_log=False):
        if senv_id is None:
            senv_id = self._senv_id
        job_id = self.idgen()
        self._db.jobq_start(job_id, self._user_id, senv_id, cmd_name, cmd_args, int(time.time()), adm_log)
        return job_id


    def end(self, job_id, cmd_exit, cmd_out, compress=True, encode=True):
        if compress:
            cmd_out = gzip.compress(cmd_out.encode('utf-8', 'replace'))
            tsadm.log.dbg('jobq.end: cmd_out compressed')
        if encode:
            cmd_out = b64encode(cmd_out)
            tsadm.log.dbg('jobq.end: cmd_out encoded')
        # 9999 and 9090 cmd_exit are used internally
        if cmd_exit == 9999 or cmd_exit == 9090:
            cmd_exit = 9000
        self._db.jobq_end(job_id, int(time.time()), cmd_exit, cmd_out)
        return job_id


    def status_update(self, job_id, status):
        return self._db.jobq_status_update(job_id, status)


    def _req(self, req_line, senv_id=None):
        if senv_id is None:
            senv_id = self._senv_id
        cmd_rtrn = 128
        cmd_out = []
        jobq_server = self._server_addr
        if self._server_addr is None:
            jobq_server = self._db.jobq_server(senv_id)
        tsadm.log.dbg('jobq_server: ', jobq_server)
        if jobq_server is None or jobq_server == '__NOT_SET__':
            ts = str(time.time())
            tsadm.log.err('NO_JOBQ_SERVER[{}]'.format(ts))
            return (64, ['NO_JOBQ_SERVER[{}]'.format(ts)])
        try:
            jobq_port = self._conf.get('JOBQ_SERVER_PORT', 6100)
            jobq_timeout = self._conf.get('JOBQ_SERVER_PORT', 15)
            tn = telnetlib.Telnet(jobq_server, jobq_port, jobq_timeout)
            tn.write('{}\n'.format(req_line).encode('utf-8', 'replace'))
            reply = tn.read_all()
            rlines = reply.decode('utf-8', 'replace').splitlines()
            tsadm.log.dbg('rlines: ', rlines)
            req_status = int(rlines[0].split(' ')[0])
            if req_status == 200:
                cmd_rtrn = int(rlines[1].split(' ')[1])
                cmd_out = rlines[3:]
            else:
                cmd_out = rlines
            tn.close()
        except Exception as e:
            ts = str(time.time())
            tsadm.log.err('JOBQ_REQ_EXECP[{}]: '.format(ts), e)
            cmd_out = ['JOBQ_REQ_EXCEP[{}]'.format(ts)]
            cmd_rtrn = 64
        return (cmd_rtrn, cmd_out)


    def cmd(self, cmd_name, args_s='', senv_id=None):
        if senv_id is None:
            site_name = self._site_name
            site_env = self._site_env
        else:
            site_name = self._db.siteenv_site_name(senv_id)
            site_env = self._db.siteenv_name(senv_id)
        req_line = '.run {} {} {} {}'.format(site_name, site_env, cmd_name, args_s)
        tsadm.log.dbg('jobq.cmd: ', req_line)
        cmd_rtrn, cmd_out = self._req(req_line, senv_id)
        self._hooks_run(cmd_name, cmd_rtrn)
        return (cmd_rtrn, cmd_out)


    def run(self, cmd_name, cmd_args, runbg=False, senv_id=None, adm_log=False):
        args_s = ''
        if type(cmd_args) == type(list()):
            args_s = ' '.join(cmd_args)
        else:
            args_s = cmd_args
        # log start
        job_id = self.start(cmd_name, args_s, senv_id=senv_id, adm_log=adm_log)
        if runbg:
            reql = '.runbg {}'.format(job_id)
            # do request
            cmd_rtrn, cmd_out = self._req(reql, senv_id=senv_id)
            cmd_out = os.linesep.join(cmd_out)
            self._hooks_run(cmd_name, cmd_rtrn)
            # log end is done by runbg command
        else:
            cmd_rtrn, cmd_out = self.cmd(cmd_name, args_s)
            cmd_out = os.linesep.join(cmd_out)
            # log end
            self.end(job_id, cmd_rtrn, cmd_out)
        return (job_id, cmd_rtrn, cmd_out)


    def cmd_hook(self, cmd_name, when, fcall, fargs=None):
        hkey = cmd_name
        if not hkey in self._cmd_hooks:
            self._cmd_hooks[hkey] = dict()
        if not when in self._cmd_hooks[hkey]:
            self._cmd_hooks[hkey][when] = list()
        self._cmd_hooks[hkey][when].append((fcall, fargs))


    def _hooks_run(self, cmd_name, cmd_rtrn):
        tsadm.log.dbg('jobq.cmd_hooks: ', self._cmd_hooks)
        if cmd_rtrn == 0:
            hkey = cmd_name
            if hkey in self._cmd_hooks:
                if 'post' in self._cmd_hooks[hkey]:
                    for hd in self._cmd_hooks[hkey]['post']:
                        f = hd[0]
                        args = hd[1]
                        tsadm.log.dbg('jobq.cmd_hooks post: ', cmd_name)
                        f(args)
                else:
                    tsadm.log.dbg('jobq.cmd_hooks: not a post hook ', hkey)
            else:
                tsadm.log.dbg('jobq.cmd_hooks post: no hook named ', hkey)
        else:
            tsadm.log.dbg('jobq.cmd_hooks post: not running hooks, cmd failed')


    def env_id(self):
        return self._senv_id


    def server_addr(self, addr=None):
        if addr is not None:
            self._server_addr = addr
        return self._server_addr
