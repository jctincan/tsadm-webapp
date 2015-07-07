# $Id: slave.py 12258 2014-12-07 00:46:14Z jrms $

from .. import RegressionTest

class RTSlave(RegressionTest):
    def configure(self):
        self.url = '/slave/1272428384/'
        self.check_regex = r'^IP address: '
        self.fail_abort = True
