import os
import sys
import os.path

__DEBUG = False
__RUN_MODE = ''
__env_mode = os.getenv('TSADM_MODE')
if __env_mode == 'test' or __env_mode == 'dev':
    __RUN_MODE = __env_mode
if __env_mode == 'dev':
    __DEBUG = True

__BASE_DIR = '/opt/tsadm'+__RUN_MODE+'/webapp'
__CONFIG_PATH = '/etc/opt/tsadm'+__RUN_MODE+'/config.json'
__MASTER_FQDN = 'master.tsadm.local'
__HOME_DIR = '/home/tsadm'+__RUN_MODE

__TSADM = {
    'RUN_MODE': __RUN_MODE,
    'BASE_DIR': __BASE_DIR,
    'CONFIG_PATH': __CONFIG_PATH,
    'DEBUG': __DEBUG,
    'CHARSET': 'utf-8',
    'LANG_CODE': 'en-gb',
    'TIME_ZONE': 'Europe/London',
    'OPENSSL': '/usr/bin/openssl',
    'SYSLOG_TAG': 'tsadm'+__RUN_MODE+'.wapp',
    'OFFLINE_FILE': __BASE_DIR+'/OFFLINE',

    'CSS_RELPATH': 'static/css/tsadm.css',
    'SLAVE_GRAPHS_BASE_URL': 'http://'+__MASTER_FQDN+'/server-graphs',

    'DB_NAME': 'tsadm'+__RUN_MODE+'db',
    'DB_USER': 'tsadm'+__RUN_MODE,
    'DB_PASS': '__NOT_SET__',

    'DJANGO_SECRET_KEY': '0GQMw7F*Fy(G_+{(K)fop06CH*mR',
    'DJANGO_CACHE_PATH': __HOME_DIR+'/django_cache',
    'DJANGO_CACHE_TIMEOUT': 3600,
    'DJANGO_CACHE_KEY_PREFIX': 'tsadm'+__RUN_MODE+':',

    'JOBQ_SERVER_PORT': 6100,
    'JOBQ_SERVER_TIMEOUT': 15,
    'JOBQ_SYSLOG_TAG': 'tsadm'+__RUN_MODE+'.jobq',

    'MASTER_SERVER': __MASTER_FQDN,
    'MASTER_SERVER_PORT': 8000,
    'MASTER_SERVER_SSL': False,

    'SITE_ENV_DOMAIN': __MASTER_FQDN,
    'SITE_HOME_BASE': __HOME_DIR+'/sites',
    'SITE_REPO_URI_TMPL': 'ssh://{user}@'+__MASTER_FQDN+'/~/{repo}.git',

    'LOG_DATE_FMT': '%b%d %H:%M:%S',
    'CUR_TIME_FMT': '%a %b %d %H:%M %Y %Z',
    'JOB_DATE_FMT': '%c %Z',

    'REGR_TESTS_ENABLE': False,
    'CLEAN_HTML_ENABLE': True,
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

def setdefault(k, v):
    if k in __TSADM.keys():
        if k != 'RUN_MODE' and k != 'BASE_DIR':
            __TSADM[k] = v

if __DEBUG:
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
    for k, v in cfg.items():
        if k in __TSADM.keys():
            __TSADM[k] = v
        else:
            print("tsadm config load: unknown key ", k, file=sys.stderr)

if os.path.exists(__CONFIG_PATH):
    __load_config()
