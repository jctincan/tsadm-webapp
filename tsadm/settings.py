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

import tsadm.config
tsadm.config.setdefault('BASE_DIR', BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = tsadm.config.get('DJANGO_SECRET_KEY', 'pUV1i7uH58cMQaQv')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = tsadm.config.get('DEBUG', False)
ALLOWED_HOSTS = [tsadm.config.get('MASTER_SERVER', 'test.tsadm.local')]
DEBUG_PROPAGATE_EXCEPTIONS = False

TEMPLATE_DEBUG = DEBUG
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

LANGUAGE_CODE = tsadm.config.get('LANG_CODE', 'en-gb')
TIME_ZONE = tsadm.config.get('TIME_ZONE', 'Europe/London')
USE_I18N = False
USE_L10N = False
USE_TZ = True
DEFAULT_CHARSET = tsadm.config.get('CHARSET', 'utf-8')
FILE_CHARSET = DEFAULT_CHARSET

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = ('/'.join([BASE_DIR, 'static']),)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': tsadm.config.get('DJANGO_CACHE_PATH', '/var/tmp/tsadmtest_cache'),
        'TIMEOUT': tsadm.config.get('DJANGO_CACHE_TIMEOUT', 15),
        'KEY_PREFIX': tsadm.config.get('DJANGO_CACHE_KEY_PREFIX', 'tsadmtest:')
    }
}
