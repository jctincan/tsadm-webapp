# $Id: config.py 12300 2014-12-12 01:04:23Z jrms $

from mysql.connector.constants import ClientFlag

from tsadm.settings import TSADM as tsadm_conf

class Config(object):
    HOST = tsadm_conf.get('DB_HOST', 'localhost')
    DATABASE = tsadm_conf.get('DB_NAME', 'tsadmdb')
    USER = tsadm_conf.get('DB_USER', 'tsadm')
    PASSWORD = tsadm_conf.get('DB_PASS', None)
    PORT = tsadm_conf.get('DB_HOST_PORT', 3306)
    CHARSET = tsadm_conf.get('DB_CHARSET', 'utf8')
    UNICODE = True
    WARNINGS = True
    TIMEOUT = tsadm_conf.get('DB_HOST_TIMEOUT', 7)

    @classmethod
    def dbinfo(self):
        return {
            'host': self.HOST,
            'database': self.DATABASE,
            'user': self.USER,
            'password': self.PASSWORD,
            'charset': self.CHARSET,
            'use_unicode': self.UNICODE,
            'get_warnings': self.WARNINGS,
            'raise_on_warnings': self.WARNINGS,
            'port': self.PORT,
            'connection_timeout': self.TIMEOUT
        }
