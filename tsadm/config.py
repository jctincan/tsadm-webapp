import os
import sys
import os.path

__RUN_MODE = ''
__env_mode = os.getenv('TSADM_MODE')
if __env_mode == 'test' or __env_mode == 'dev':
    __RUN_MODE = __env_mode

__BASE_DIR = '/opt/tsadm'+__RUN_MODE
__CONFIG_PATH = '/etc/opt/tsadm'+__RUN_MODE+'/config.json'

__TSADM = {
    'RUN_MODE': __RUN_MODE,
    'BASE_DIR': __BASE_DIR,
    'DEBUG': True,
    'CHARSET': 'utf-8',
    'LANG_CODE': 'en-gb',
    'TIME_ZONE': 'Europe/London',
    'DJANGO_SECRET_KEY': '0GQMw7F*Fy(G_+{(K)fop06CH*mR+!,*\Q]S&Mg4|y(l;?}4|~',
    'DJANGO_CACHE_PATH': '/var/tmp/tsadm'+__RUN_MODE+'_cache',
    'DJANGO_CACHE_TIMEOUT': 3600,
    'DJANGO_CACHE_KEY_PREFIX': 'tsadm'+__RUN_MODE+':',
    'OPENSSL': '/usr/bin/openssl',
    'JOBQ_SERVER_PORT': 6100,
    'JOBQ_SERVER_TIMEOUT': 15,
    'JOBQ_SYSLOG_TAG': 'tsadm'+__RUN_MODE+'.jobq',
    'MASTER_SERVER': 'dev.tsadm.local',
    'MASTER_SERVER_PORT': 8000,
    'MASTER_SERVER_SSL': False,
    'SITE_ENV_DOMAIN': 'dev.tsadm.local',
    'SITE_HOME_BASE': '/home/tsadm'+__RUN_MODE+'/sites',
    'LOG_DATE_FMT': '%b%d %H:%M:%S',
    'CUR_TIME_FMT': '%a %b %d %H:%M %Y %Z',
    'JOB_DATE_FMT': '%c %Z',
    'SYSLOG_TAG': 'tsadm'+__RUN_MODE+'.wapp',
    'REGR_TESTS_ENABLE': True,
    'CLEAN_HTML_ENABLE': True,
    'SLAVE_GRAPHS_BASE_URL': 'http://dev.tsadm.local/server-graphs',
    'DB_NAME': 'tsadm'+__RUN_MODE+'db',
    'DB_USER': 'tsadm'+__RUN_MODE,
    'DB_PASS': 'M34iKsymcyHL3hsU',
    'CSS_RELPATH': 'static/css/tsadm.css',
    'OFFLINE_FILE': os.path.join(__BASE_DIR, 'OFFLINE'),
}

def get(arg, default=None):
    return __TSADM.get(arg, default)

def update(d):
    return __TSADM.update(d)

def export():
    r = list()
    for sk in sorted(__TSADM.keys()):
        if sk.lower().find("pass") > 0 or sk.lower().find("secret") > 0:
            r.append((sk, '__HIDDEN__'))
        else:
            r.append((sk, __TSADM.get(sk)))
    return r

def __set_get(arg_name, arg=None):
    if arg is not None:
        __TSADM[arg_name] = arg
    return __TSADM.get(arg_name)

def debug(enable=None):
    return __set_get('DEBUG', enable)

def base_dir(dpath=None):
    return __set_get('BASE_DIR', dpath)

def charset(cs=None):
    return __set_get('CHARSET', cs)

def django_secret_key(sk=None):
    return __set_get('DJANGO_SECRET_KEY', sk)

def django_cache_path(arg=None):
    return __set_get('DJANGO_CACHE_PATH', arg)

def django_cache_timeout(arg=None):
    return __set_get('DJANGO_CACHE_TIMEOUT', arg)

def django_cache_key_prefix(arg=None):
    return __set_get('DJANGO_CACHE_KEY_PREFIX', arg)

def master_fqdn(fqdn=None):
    return __set_get('MASTER_SERVER', fqdn)

def lang_code(lc=None):
    return __set_get('LANG_CODE', lc)

def time_zone(tz=None):
    return __set_get('TIME_ZONE', tz)

if debug():
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

def __load_config():
    import json
    cfg = dict()
    try:
        fh = open(__CONFIG_PATH, 'r')
        cfg = json.load(fh)
        fh.close()
    except Exception as e:
        print("tsadm config load:", __CONFIG_PATH, e, file=sys.stderr)
    print("LOAD:", cfg, file=sys.stderr)
    for k, v in cfg.items():
        if k in __TSADM.keys():
            __TSADM[k] = v
        else:
            print("tsadm config load: unknown key ", k, file=sys.stderr)

if debug(): print('CONFIG_PATH:', __CONFIG_PATH, file=sys.stderr)
if os.path.exists(__CONFIG_PATH):
    __load_config()
