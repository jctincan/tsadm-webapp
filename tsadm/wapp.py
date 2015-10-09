import os
import os.path
import subprocess
import tempfile
import time
import hashlib
import json
import lxml.html
import html


from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse

import tsadm.log
import tsadm.config
from tsadm.db import TSAdmDB
from tsadm.db import TSAdmDBVersionError
from tsadm.jobq import TSAdmJobQ
from tsadm.user import TSAdmUser
from tsadm.site import TSAdmSite


class TSAdmUMesg:
    _mesgs = None

    def __init__(self):
        self._mesgs = list()

    def inf(self, mesg):
        self._mesgs.append(('INF', mesg))

    def warn(self, mesg):
        self._mesgs.append(('WARN', mesg))

    def err(self, mesg):
        self._mesgs.append(('ERR', mesg))

    def tmpl_data(self):
        r = list()
        for m in self._mesgs:
            l = {
                'prio': m[0].lower(),
                'mesg': m[1],
            }
            r.append(l)
        return r


class TSAdmWApp:
    conf = None
    db = None
    log = None
    user = None
    site = None
    jobq = None
    umesg = None
    version = None
    debug = None
    devmode = False
    regr_tests = None
    encoding = None
    _req = None
    _err_code = 500
    _err_msg = ''
    _start_tstamp = None


    def __load_conf(self):
        # -- load settings
        self.conf = tsadm.config
        self.encoding = self.conf.get('CHARSET', 'utf-8')
        self.regr_tests = self.conf.get('REGR_TESTS_ENABLE', False)
        vfile = os.path.join(self.conf.get('BASE_DIR'), 'VERSION.txt')
        try:
            fh = open(vfile, 'r', encoding=self.encoding)
            self.version = fh.readline().strip()
            fh.close()
        except:
            self.version = 'ERR'
        # -- dev mode
        if self.conf.get('RUN_MODE', '') == 'dev':
            self.debug = True
            self.devmode = True
            self.conf.update({
                'DEV_CLIENT_CERT': self.conf.get('BASE_DIR')+'/dev-client-cert.crt'
            })
        # MiddleWare conf
        TSAdmWAppMiddleWare.debug = self.debug
        TSAdmWAppMiddleWare.encoding = self.encoding
        TSAdmWAppMiddleWare.clean_enable = self.conf.get('CLEAN_HTML_ENABLE', False)
        TSAdmWAppMiddleWare.version = self.version
        TSAdmWAppMiddleWare.conf = self.conf


    def __start_log(self, req):
        # -- log
        self.log = tsadm.log
        self.log.log_open(self.conf.get('SYSLOG_TAG', 'tsadm.wapp'))
        self.log.inf('START - {}'.format(req.path_info))
        #~ self.log.dbg('META: ', req.META)
        self.log.dbg('req.method: ', req.method)


    def start(self, req, site_name, env_name=None, unlock_req=False, acclvl='USER'):
        self._start_tstamp = time.time()
        if env_name == None and site_name.startswith('__'):
            env_name = site_name
        self._req = req
        # -- load settings
        self.__load_conf()
        # -- umesg
        self.umesg = TSAdmUMesg()
        # -- log
        self.__start_log(req)
        self.log.dbg('RUN_MODE: ', self.conf.get('RUN_MODE'))
        # -- offline mode
        if self.__offline_mode():
            self._err_code = 904
            self._err_msg = 'Offline mode enabled'
            self.log.wrn('Offline mode is enabled')
            return False
        # -- db
        try:
            self.db = TSAdmDB()
        except TSAdmDBVersionError as e:
            self._err_code = 500
            self._err_msg = 'database upgrade required: {}'.format(e.db_version)
            self.log.err('start: ', e)
            return False
        except Exception as e:
            self._err_code = 500
            self._err_msg = str('database connection error')
            self.log.err('start: ', e)
            return False
        # -- pre flight checks
        if not self._pre_flight_check():
            self.log.err('pre_flight_check: ', self._err_code)
            self.log.err(self._err_msg)
            return False
        # -- user auth
        self.user = TSAdmUser(self.log, self.db, self.conf, self.umesg)
        if not self._auth_check():
            self.log.err('auth_check: ', self._err_code)
            self.log.err(self._err_msg)
            return False
        # -- user load
        if not self.user.load():
            self._err_code = 401
            self._err_msg = 'could not load user'
            self.log.err('user_load: ', self._err_code)
            self.log.err(self._err_msg)
            return False
        # -- check user access level
        self.log.dbg('check_acclvl: ', acclvl)
        if not self._user_acclvl(acclvl):
            self.log.err('user_acclvl: ', self._err_code)
            self.log.err(self._err_msg)
            return False
        # -- site init
        self.site = TSAdmSite(self.log, self.db, self.user, self.conf)
        if not self.site.load(site_name, env_name):
            self._err_code = 400
            self._err_msg = 'could not load: {}.{}'.format(site_name, env_name)
            self.log.err('site.load: ', self._err_code)
            self.log.err(self._err_msg)
            return False
        # -- site env load
        if self.site.env.id < self.db.SITEENV_ID_MIN or site_name.startswith('__'):
            # internal page
            self.log.inf('stop site loading: internal page')
        else:
            # user site env acl checks
            if not self.site.env.acl_check():
                self._err_code = 401
                self._err_msg = 'unauthorized site env'
                return False
            # check site env locked
            senv_locked, err_code, err_msg = self.site.env.lock_check(unlock_req)
            if senv_locked:
                self._err_code = err_code
                self._err_msg = err_msg
                return False
            # check site env claimed
            if not self.site.env.claim_check():
                self._err_code = 903
                self._err_msg = 'site claimed by {}'.format(self.site.env.claimed_by)
                return False
            # check if site env is live
            self.log.dbg('site.env.is_live=', self.site.env.is_live)
            if self.site.env.is_live:
                self.umesg.warn('you are working on a LIVE environment')
                self.log.inf('LIVE env')
        # -- jobq
        self.jobq = TSAdmJobQ(self.db, self.user.id, self.site.env.id, self.site.name, self.site.env.name, self.conf)
        return True


    def _endlog(self, td, took):
        self.log.dbg('endlog: ', took)
        if self.db is not None:
            try:
                user_id = td['user']['id']
            except:
                user_id = None
            try:
                page_uri = td['page']['uri']
            except:
                page_uri = 'ERROR'
            if user_id is not None:
                self.db.activity_log_put(self._start_tstamp, took, user_id, page_uri)
                # -- user last seen
                self.db.user_last_seen(user_id, time.time())
            self.db.close()


    def end(self, tmpl_data=None):
        wapp_took = '{:.3f}s'.format(time.time() - self._start_tstamp)
        if tmpl_data is None:
            self._endlog(self.tmpl_data(), wapp_took)
            self.log.wrn('OLD IMPLEMENTATION: end call')
            self.log.inf('END1 - ', wapp_took)
            self.log.log_close()
            return wapp_took
        else:
            tmpl_data['umesg'] = self.umesg.tmpl_data()
            tmpl_data['took'] = wapp_took
            tmpl_data['debug'] = None
            if self.debug:
                tmpl_cp = tmpl_data.copy()
                tmpl_data['debug'] = {'tmpl': json.dumps(tmpl_cp, indent=4)}
            #~ self.log.dbg('tmpl_data=', tmpl_data)
            self._endlog(tmpl_data, wapp_took)
            self.log.inf('END2 - ', wapp_took)
            self.log.log_close()
            return tmpl_data


    def error_page(self, err_code=None, err_msg=None):
        if err_code is None:
            err_code = self._err_code
        if err_msg is None:
            err_msg = self._err_msg
        tmpl_data = self.tmpl_data()
        status_code = err_code
        if err_code == 901:
            status_code = 401
            tmpl = 'site/locked.html'
        elif err_code == 902:
            status_code = 401
            tmpl = 'site/cant_unlock.html'
        elif err_code == 903:
            status_code = 401
            tmpl = 'site/claimed.html'
        elif err_code == 904:
            status_code == 200
            tmpl = 'error/offline.html'
        else:
            tmpl = 'error/{}.html'.format(str(err_code))
            tmpl_data['err_msg'] = err_msg
        self.log.err('{}[{}] - {}'.format(status_code, err_code, err_msg))
        tmpl_data['took'] = self.end()
        return render(self._req, tmpl, tmpl_data, status=status_code, content_type='text/html; charset={}'.format(self.encoding))


    def _pre_flight_check(self):
        if not os.access(self.conf.get('OPENSSL', None), os.F_OK | os.X_OK):
            self._err_msg = 'openssl command not found'
            return False
        if not os.access(self.conf.get('SSH_KEYGEN', None), os.F_OK | os.X_OK):
            self._err_msg = 'openssl command not found'
            return False
        return True


    def _auth_check(self):
        client_cert = self._req.META.get('SSL_CLIENT_CERT', '_NONE_')
        scheme = self._req.META.get('UWSGI_SCHEME', 'http')

        if self.debug:
            scheme = 'https'
            try:
                fh = open(self.conf.get('DEV_CLIENT_CERT', None), 'r', encoding='utf-8')
                client_cert = fh.read()
                fh.close()
            except:
                pass

        if scheme != 'https':
            self._err_code = 401
            self._err_msg = 'ssl access only'
            return False

        if client_cert == '_NONE_':
            self._err_code = 401
            self._err_msg = 'client cert required'
            return False

        tmp_f = tempfile.NamedTemporaryFile('w')
        tmp_f.file.write(client_cert)
        tmp_f.file.flush()

        openssl_cmd = '{} x509 -in {} -noout -email -fingerprint -startdate -enddate 2>/dev/null'.format(self.conf.get('OPENSSL', None), tmp_f.name)
        cert_data = subprocess.check_output(openssl_cmd, shell=True).decode('utf-8', 'replace').splitlines()
        del tmp_f

        if not self.user.auth_check(cert_data):
            self._err_code = 401
            self._err_msg = 'bad user: '+self.user.name
            return False
        return True


    def _user_acclvl(self, check_level):
        self._err_code = 401
        check = self.user.acclvl_check(check_level)
        if check == 'WRONG':
            self._err_msg = 'wrong access level'
            return False
        elif check == 'USER_DISABLE':
            self._err_msg = 'disabled user'
            return False
        elif check == 'PAGE_DISABLE':
            self._err_msg = 'disabled page'
            return False
        elif check == 'CHECK_WRONG':
            self._err_msg = 'wrong check access level'
            return False
        elif check == 'LOW':
            self._err_msg = 'low access level'
            return False
        elif check == 'OK':
            return True
        self._err_msg = 'access level check failed'
        return False


    def __css_version(self):
        fpath = os.path.join(self.conf.get('BASE_DIR'), self.conf.get('CSS_RELPATH'))
        stat = os.stat(fpath)
        return str(stat.st_mtime)


    def __css_relpath(self):
        return '/'+self.conf.get('CSS_RELPATH')


    def tmpl_data(self):
        d = dict()
        d['appname'] = self.conf.get('APPNAME')
        d['version'] = self.version
        d['date_time'] = time.strftime(self.conf.get('CUR_TIME_FMT'), time.localtime())
        d['page'] = {
            'uri': self._req.get_full_path(),
            'title': self._req.path_info
        }
        d['regr_tests_enable'] = self.regr_tests
        d['charset'] = self.encoding
        d['devmode'] = self.debug
        if self.user is None:
            d['user'] = dict()
        else:
            d['user'] = self.user.tmpl_data()
        if self.site is not None:
            d['site'] = self.site.tmpl_data()
        d['css_relpath'] = self.__css_relpath()
        d['css_version'] = self.__css_version()
        prot = 'http'
        if self._req.is_secure():
            prot = 'https'
        d['base_href'] = '{}://{}/'.format(prot, self._req.get_host())
        return d


    def tmpl_regr_tests_data(self, data_in):
        if self.regr_tests:
            data = [
                self.site.name.encode(),
                self.site.env.name.encode(),
                #~ self.user.name.encode(),
            ]
            for d in data_in:
                data.append(str(d).encode())
            ds = b':'.join(sorted(data))
            del data_in
            del data
            sha1 = hashlib.sha1()
            sha1.update(ds)
            d = {
                'data': ds.decode(),
                'digest': sha1.hexdigest()
            }
            del sha1
            return {'regr_tests': d}
        else:
            return {'regr_tests': None}


    def _cache_key(self, ckey):
        # just in case we want to add/remove something...
        return ckey


    def cache_set(self, ckey, set_val, ttl=None):
        if ttl is not None:
            return cache.set(self._cache_key(ckey), set_val, ttl)
        else:
            return cache.set(self._cache_key(ckey), set_val)


    def cache_get(self, ckey):
        return cache.get(self._cache_key(ckey))


    def cache_del(self, ckey):
        return cache.delete(self._cache_key(ckey))


    def nsresolve(self, fqdn):
        ckey = 'slave:nsresolve:{}'.format(fqdn)
        ipaddr = self.cache_get(ckey)
        if ipaddr is not None:
            return ipaddr
        cmd = '/usr/bin/getent hosts {} | /usr/bin/cut -d" " -f1'.format(fqdn)
        status, ipaddr = subprocess.getstatusoutput(cmd)
        ipaddr = ipaddr.strip()
        if int(status) != 0:
            return 'GETENT_FAILED'
        elif ipaddr == '':
            return 'IPADDR_NOT_FOUND'
        else:
            self.cache_set(ckey, ipaddr, 3600)
            return ipaddr


    def __offline_mode(self):
        return os.path.exists(self.conf.get('OFFLINE_FILE'))


    def json_response(self, json_data={}):
        if self.debug:
            import json
            from django.http import HttpResponse
            self.end(tmpl_data={})
            return HttpResponse(json.dumps(json_data, indent=2), content_type='application/json')
        self.end(tmpl_data={})
        return JsonResponse(json_data)


    def slug(self, *items):
        return ''.join(items)+self.conf.get('RUN_MODE', '').upper()


class TSAdmWAppMiddleWare:
    debug = None
    encoding = None
    clean_enable = None
    version = None
    conf = None


class TSAdmWAppCleanHTML(TSAdmWAppMiddleWare):

    def __css_validate(self, content):
        tsadm.log.dbg('BASE_DIR: ', tsadm.config.get('BASE_DIR'))
        css_fpath = os.path.join(tsadm.config.get('BASE_DIR'), tsadm.config.get('CSS_RELPATH'))
        tsadm.log.dbg('css_fpath: ', css_fpath)
        fh = open(css_fpath, 'rb')
        css_content = fh.read()
        fh.close()
        return content.replace(b'[[TSADM_CSS_VALIDATE_CONTENT]]', css_content)

    def __html_validate(self, resp):
        if self.debug:
            resp.content = self.__css_validate(resp.content)
            resp.content = resp.content.replace(b'[[TSADM_HTML_VALIDATE_CONTENT]]', html.escape(resp.content.decode()).encode())
        return resp

    def process_response(self, req, resp):
        if self.debug:
            #~ tsadm.log.dbg('TSAdmWAppCleanHTML:', type(resp), dir(resp))
            #~ tsadm.log.dbg('TSAdmWAppCleanHTML:', resp._handler_class)
            #~ tsadm.log.dbg('TSAdmWAppCleanHTML:', resp._headers)
            tsadm.log.dbg('TSAdmWAppCleanHTML:', resp.get('content-type'))
        if self.clean_enable and not resp.streaming:
            ctype = resp.get('content-type')
            if resp.content != b'' and ctype.startswith('text/html'):
                try:
                    resp.content = lxml.html.tostring(lxml.html.document_fromstring(resp.content.decode()), pretty_print=True, include_meta_content_type=True, encoding=self.encoding)
                    resp.content = b'<!DOCTYPE html>\n' + resp.content
                except Exception as e:
                    tsadm.log.err('TSAdmWAppCleanHTML: ', e)
        return self.__html_validate(resp)


class TSAdmWAppResponseHeaders(TSAdmWAppMiddleWare):
    def process_response(self, req, resp):
        appname = self.conf.get('APPNAME').capitalize()
        resp['X-'+appname+'-Version'] = self.version
        sts = self.conf.get('HTTP_HEADER_STS')
        if sts is not None and sts != '':
            resp['Strict-Transport-Security'] = sts
        ccontrol = self.conf.get('HTTP_HEADER_CACHE_CONTROL')
        if ccontrol is not None and ccontrol != '':
            resp['Cache-Control'] = ccontrol
        return resp
