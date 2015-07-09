# $Id: config.py 12300 2014-12-12 01:04:23Z jrms $

import tsadm.config
from mysql.connector.constants import ClientFlag

class Config(object):
    HOST = tsadm.config.get('DB_HOST', 'localhost')
    DATABASE = tsadm.config.get('DB_NAME', 'tsadmdb')
    USER = tsadm.config.get('DB_USER', 'tsadm')
    PASSWORD = tsadm.config.get('DB_PASS', None)
    PORT = tsadm.config.get('DB_HOST_PORT', 3306)
    CHARSET = tsadm.config.get('DB_CHARSET', 'utf8')
    UNICODE = True
    WARNINGS = True
    TIMEOUT = tsadm.config.get('DB_HOST_TIMEOUT', 7)

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
