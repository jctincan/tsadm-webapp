# $Id: slave.py 12258 2014-12-07 00:46:14Z jrms $

from .. import RegressionTest

class RTSlave(RegressionTest):
    def configure(self):
        self.url = '/slave/2663516195/'
        self.check_regex = r'^IP address: 127\.0\.0\.1$'
        self.fail_abort = True
