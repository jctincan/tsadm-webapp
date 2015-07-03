# $Id: settings.py 12979 2015-07-01 21:21:31Z jrms $
"""
Django settings for tsadm project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rf=x18&ba&md&ntlxf=n!p^^4&n0pkpz_+5!&gbs_5wr0!885w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['tsadm.local']
DEBUG_PROPAGATE_EXCEPTIONS = False

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = ('/'.join([BASE_DIR, 'templates']),)
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',)
TEMPLATE_STRING_IF_INVALID = 'TMPL_MISS:%s'

# Application definition

INSTALLED_APPS = (
    #'django.contrib.admin',
    #'django.contrib.auth',
    #'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django_extensions',
    'tsadm.site',
    'tsadm.git',
    'tsadm.rsync',
    'tsadm._mysql',
    'tsadm.help',
    'tsadm.jobq',
    'tsadm.user',
    'tsadm.slave',
    'tsadm.admin',
    'tsadm.ansible',
)

MIDDLEWARE_CLASSES = (
    'tsadm.wapp.TSAdmWAppCleanHTML',
    #'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tsadm.urls'
WSGI_APPLICATION = 'tsadm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Using tsadm.db module as at the time of starting this project Django
# didn't have support for mysql under python3.
# tsadm.db uses mysql.connector

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': '',
        'NAME': '',
    }
}

#SESSION_ENGINE = 'django.contrib.sessions.backends.file'
#SESSION_SAVE_EVERY_REQUEST = True

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = False
USE_L10N = False
USE_TZ = True
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = DEFAULT_CHARSET

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = ('/'.join([BASE_DIR, 'static']),)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/tsadmdev_cache',
        'TIMEOUT': 60*2,
        'KEY_PREFIX': 'tsadm:'
    }
}

# TSAdm settings
TSADM = {
    'BASE_DIR': BASE_DIR,
    'CHARSET': DEFAULT_CHARSET,
    'OPENSSL': '/usr/bin/openssl',
    'JOBQ_SERVER_PORT': 6100,
    'JOBQ_SERVER_TIMEOUT': 15,
    'JOBQ_SYSLOG_TAG': 'tsadm-dev.jobq',
    'MASTER_SERVER': 'tsadm.chroot',
    'MASTER_SERVER_PORT': 8000,
    'MASTER_SERVER_SSL': False,
    'SITE_ENV_DOMAIN': 'tsadm.tincan.co.uk',
    'SITE_HOME_BASE': '/home/tsadm/sites',
    'LOG_DATE_FMT': '%b%d %H:%M:%S',
    'CUR_TIME_FMT': '%a %b %d %H:%M %Y %Z',
    'JOB_DATE_FMT': '%c %Z',
    'SYSLOG_TAG': 'tsadm-dev.wapp',
    'REGR_TESTS_ENABLE': True,
    'CLEAN_HTML_ENABLE': True,
    'SLAVE_GRAPHS_BASE_URL': 'http://localhost/server-graphs',
    'DB_NAME': 'tsadmdevdb',
    'DB_USER': 'tsadmdev',
    'DB_PASS': 'M34iKsymcyHL3hsU',
    'OFFLINE_FILE': os.path.join(BASE_DIR, 'tsadm.offline'),
    'CSS_RELPATH': 'static/css/tsadm.css',
}
TSADM_DEBUG = {
    'DEBUG_DISABLES_CACHE': True,
    'DEV_CLIENT_CERT': BASE_DIR+'/dev-client-cert.crt',
    'SITE_ENV_DOMAIN': 'tsadm.local',
}
if DEBUG:
    TSADM.update(TSADM_DEBUG)
    if TSADM.get('DEBUG_DISABLES_CACHE', True) is True:
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }
        }
