# $Id: rsync.py 12295 2014-12-11 14:47:05Z jrms $

import time
from .. import RegressionTest


class RTRsync(RegressionTest):
    def configure(self):
        self.url = '/files/regr/test/'
        self.check_digest = '80ce52797867108c35e545894228ce46e964eef5'
        self.fail_abort = False


class RTRsyncDirs(RegressionTest):
    def configure(self):
        self.url = '/jobq/ce/regr/test/'
        self.check_regex = r'^<!-- CMD_STATUS=rsync\.dirs:(0|1) -->$'
        self.post_data = {
            'tsadm_cmd': 'rsync.dirs',
            'tsadm_cmd_args_encode': 'LS1yc3luY19zb3VyY2VzPWRvY3Jvb3Qvc2l0ZXMvZGVmYXVsdC9maWxlcyAtLWhvc3Rfb3JpZz1sb2NhbGhvc3QgLS1yc3luY19kZXN0X2Vudj1sb2NhbGhvc3Q6OnJlZ3I6OmRldg=='
        }
        self.fail_reload = 3
        self.fail_reload_wait = 3
