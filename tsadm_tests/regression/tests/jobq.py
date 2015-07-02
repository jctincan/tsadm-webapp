# $Id: jobq.py 12244 2014-12-04 18:07:07Z jrms $

from .. import RegressionTest


class RTJobQCommandConfirm(RegressionTest):
    def configure(self):
        self.url = '/jobq/cc/regr/test/'
        self.check_regex = r'^[\s]+Confirm running command against <b>regr\.test</b> environment\.<br'
        self.post_data = {'tsadm_cmd': 'git.pull'}
        self.fail_abort = True
