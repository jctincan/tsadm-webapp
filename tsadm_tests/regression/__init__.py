
import http.client
import urllib.parse
import re
import sys
import time
import ssl
import os


TSADM_MASTER = 'tincandev.local'
TSADM_MASTER_PORT = 8000

LOCATION_REDIRECT_MAX = 10
FAIL_RELOAD_MAX = 10


class RTGlobal:
    bootstrap = None
    rt_map = None
    conn = None
    failed = None
    rt_loaded_no = None
    rt_run_no = None
    rt_fail_no = None
    report_rt_name_width = None
    prev_url = None
    ssl = None
    verbose = None


class RegressionTestManager:
    _start_at = None
    _sys_argv = None
    _load_tests = None
    _test_loader = None
    err_msg = None
    run_wait = None

    def __init__(self, sys_argv=[]):
        self._start_at = time.time()
        self._sys_argv = sys_argv
        self._load_tests = list()
        self.run_wait = 0

    def __server_connect(self):
        conn = http.client.HTTPConnection(TSADM_MASTER, TSADM_MASTER_PORT)
        return conn

    def __server_ssl_connect(self):
        cafile = 'etc/certs/tsadmca.pem'
        cert_file = 'etc/certs/regrtest.pem'
        key_file = cert_file
        cntxt = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        cntxt.load_verify_locations(cafile=cafile)
        conn = http.client.HTTPSConnection(TSADM_MASTER, 443, key_file=key_file, cert_file=cert_file, context=cntxt)
        return conn

    def __list_tests(self):
        for tname in sorted(self._load_tests):
            print(tname)

    def __check_sys_argv(self):
        if '--list' in self._sys_argv:
            self.__list_tests()
            sys.exit(0)
        load_tests_cleaned = False
        for arg in self._sys_argv:
            if arg.startswith('--run='):
                if not load_tests_cleaned:
                    self._load_tests = list()
                    load_tests_cleaned = True
                tn = arg.split('=')[1]
                self._load_tests.append(tn)
        RTGlobal.verbose = 1
        if '-v' in sys.argv:
            RTGlobal.verbose = 2
        elif '-vv' in sys.argv:
            RTGlobal.verbose = 3

    def bootstrap(self):
        RTGlobal.rt_map = dict()
        RTGlobal.failed = False
        RTGlobal.rt_loaded_no = 0
        RTGlobal.rt_run_no = 0
        RTGlobal.rt_fail_no = 0
        RTGlobal.ssl = os.getenv('TSADM_REGR_TESTS_SSL', False)
        if RTGlobal.ssl:
            RTGlobal.conn = self.__server_ssl_connect()
        else:
            RTGlobal.conn = self.__server_connect()
        print(RTGlobal.conn.host, RTGlobal.conn.port)
        from . import tests
        self._load_tests = tests.config.LOAD_TESTS.keys()
        self._test_loader = tests.load
        self.__check_sys_argv()
        RTGlobal.bootstrap = True

    def end(self):
        RTGlobal.conn.close()
        print('{:9s} {:6s} {:0>7.3f}s loaded:{} run:{} fail:{}'.format('', 'STAT', float(time.time() - self._start_at), RTGlobal.rt_loaded_no, RTGlobal.rt_run_no, RTGlobal.rt_fail_no, rtnw=RTGlobal.report_rt_name_width))

    def run_all(self):
        run_no = 0
        for tk in sorted(RTGlobal.rt_map.keys()):
            t = RTGlobal.rt_map.get(tk)
            run_no += 1
            print('{:0>3}/{:0>3} - '.format(run_no, RTGlobal.rt_loaded_no), end='')
            if not t.run():
                if t.fail_abort:
                    return False
            RTGlobal.prev_url = t.url
            del t
            del RTGlobal.rt_map[tk]
            # -- sleep a bit
            time.sleep(self.run_wait)
        return True

    def load_tests(self):
        RTGlobal.report_rt_name_width = -1
        for tname in sorted(self._load_tests):
            try:
                rt = self._test_loader(tname)
                rt.configure()
                rt.config_check()
                RTGlobal.rt_map[tname] = rt
                RTGlobal.rt_loaded_no += 1
                tname_len = len(tname)
                if tname_len > RTGlobal.report_rt_name_width:
                    RTGlobal.report_rt_name_width = tname_len
                #~ print('LOADED {}'.format(repr(rt)))
            except Exception as e:
                self.err_msg = e
                return False
        #~ print('rt name longest:', RTGlobal.report_rt_name_width)
        return True

    def failed(self):
        return RTGlobal.failed


class RegressionTest:
    _conn = None
    _lineno = None
    _start_at = None
    _resp_headers = None
    _location_redirect = None
    _locations_hist = None
    _clines = None
    resp_status = None
    name = None
    url = None
    check_regex = None
    check_reverse = None
    resp_reason = None
    check_re_match = None
    check_match_line = None
    fail_abort = None
    post_data = None
    check_digest = None
    ssl = None
    verbose = None
    fail_reload = None
    fail_reload_wait = None
    fail_reload_count = None

    def __init__(self, name):
        self.name = name
        self.check_reverse = False
        self._conn = RTGlobal.conn
        self._location_redirect = 0
        self._locations_hist = list()
        self.fail_abort = False
        self.ssl = RTGlobal.ssl
        self.verbose = RTGlobal.verbose
        self.fail_reload = False
        self.fail_reload_wait = 0
        self.fail_reload_count = 0

    def __repr__(self):
        return 'RT<{}>'.format(self.name)

    def __check_redirect(self, cur_loc, headers):
        if self._location_redirect >= LOCATION_REDIRECT_MAX:
            raise RuntimeError('location redirect limit reached:', self._location_redirect)
        for hk, hv in headers:
            if hk == 'Location':
                nl = hv.replace('http://'+TSADM_MASTER+':'+str(TSADM_MASTER_PORT), '', 1)
                self._locations_hist.append('{}:{}'.format(self._location_redirect, cur_loc))
                self._location_redirect += 1
                if self.verbose >= 3:
                    print('DBG - redirect:', nl, file=sys.stderr)
                return nl
        return None

    def get_content(self, url=None, redirect=False, fail_reload=False):
        if url is not None:
            self.url = url
        if self.verbose >= 3:
            print('DBG - get_content:', self.url, file=sys.stderr)
        method = 'GET'
        if self.post_data is not None and not redirect and not fail_reload:
            method = 'POST'
        if method == 'POST':
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/plain'
            }
            params = urllib.parse.urlencode(self.post_data)
            self._conn.request('POST', self.url, params, headers)
        else:
            self._conn.request('GET', self.url)
        resp = self._conn.getresponse()
        self.resp_status = resp.status
        self.resp_reason = resp.reason
        self._resp_headers = resp.getheaders()
        location = self.__check_redirect(self.url, self._resp_headers)
        if location is not None:
            return self.get_content(location, redirect=True)
        content = resp.read().decode()
        return content.split('\n')

    def get_prev_url(self):
        return RTGlobal.prev_url

    def config_check(self):
        if self.url is None:
            raise RuntimeError('{}: config url not set'.format(repr(self)))
        elif self.check_regex is None:
            if self.check_digest is None:
                raise RuntimeError('{}: check_regex or check_digest config must be set'.format(repr(self)))

    def configure(self):
        raise RuntimeError('{}.configure: not implemented'.format(repr(self)))

    def __info_line(self):
        il = '{:0>7.3f}s line:{}'.format(time.time() - self._start_at, self.check_match_line)
        return il

    def __fail_report(self):
        rfname = 'fail-report-{}.txt'.format(self.name)
        print('{:9s} FAIL++ {}'.format('', rfname, rtnw=RTGlobal.report_rt_name_width))
        fh = open(rfname, 'w')
        print(RTGlobal.conn.host, RTGlobal.conn.port, file=fh)
        print(repr(self), file=fh)
        for an in sorted(dir(self)):
            if not an.startswith('_'):
                av = str(getattr(self, an))
                if av is not None and not av.startswith('<bound method '):
                    print('{}="{}"'.format(an, av), file=fh)
        print('location_redirect="{}"'.format(self._location_redirect), file=fh)
        for lh in sorted(self._locations_hist):
            print('location_hist="{}"'.format(lh), file=fh)
        print('=== HEADERS START ===', file=fh)
        for hk, hv in self._resp_headers:
            print('{}: {}'.format(hk, hv), file=fh)
        print('=== HEADERS END ===', file=fh)
        print('=== CONTENT START ===', file=fh)
        for line in self._clines:
            print(line, file=fh)
        print('=== CONTENT END ===', file=fh)
        fh.close()

    def __parse_content(self, clines):
        self._lineno = 0
        re_check = None
        if self.check_digest is not None:
            re_digest = r'^<!-- TSADM_REGR_TESTS:DIGEST:{} -->$'
            re_check = re.compile(re_digest.format(self.check_digest))
        else:
            re_check = re.compile(self.check_regex)
        self._clines = clines
        if self.verbose >= 3:
            print('DBG - parse_content:', self.url, file=sys.stderr)
        for line in self._clines:
            if self.verbose >= 3:
                print('DBG - parse line:', line, file=sys.stderr)
            self._lineno += 1
            re_match = re_check.match(line)
            if re_match:
                self.check_re_match = re_match
                self.check_match_line = self._lineno
                return not self.check_reverse
        if self.fail_reload:
            if self.fail_reload_count >= FAIL_RELOAD_MAX:
                raise RuntimeError('FAIL_RELOAD_MAX[{}] limit reached: {}'.format(FAIL_RELOAD_MAX, self.fail_reload_count))
            elif self.fail_reload_count >= self.fail_reload:
                return self.check_reverse
            self.fail_reload_count += 1
            time.sleep(self.fail_reload_wait)
            _clines = self.get_content(fail_reload=True)
            return self.__parse_content(_clines)
        return self.check_reverse

    def pre_run(self):
        # if the child re-implements it, it will do something...
        pass

    def post_run(self):
        # if the child re-implements it, it will do something...
        pass

    def run(self):
        self._start_at = time.time()
        print('{:{rtnw}s}'.format(self.name, rtnw=RTGlobal.report_rt_name_width), end='', flush=True)
        RTGlobal.rt_run_no += 1
        # -- pre run
        self.pre_run()
        # -- run
        clines = self.get_content()
        if self.__parse_content(clines):
            print(' {:6s} {}'.format('OK', self.__info_line()))
            if self.verbose >= 2:
                print('{:9s} {:6s} \'{}\''.format('', 'OK++', self.check_re_match.string, rtnw=RTGlobal.report_rt_name_width))
            # -- post run
            self.post_run()
            return True
        else:
            print(' {:6s} {}'.format('FAIL', self.__info_line()))
            self.__fail_report()
            RTGlobal.failed = True
            RTGlobal.rt_fail_no += 1
            # -- post run
            self.post_run()
            return False

    def line_regex_get(self, clines, regex, rgroup):
        re_check = re.compile(regex)
        for line in clines:
            re_match = re_check.match(line)
            if re_match:
                return re_match.group(rgroup)
        return None
