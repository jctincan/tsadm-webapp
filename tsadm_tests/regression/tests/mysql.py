
from .. import RegressionTest

class RTMySQLSync(RegressionTest):
    def configure(self):
        self.url = '/jobq/ce/regr/test/'
        self.check_regex = r'^<!-- CMD_STATUS=mysql\.sync:(0|1) -->$'
        self.post_data = {
            'tsadm_cmd': 'mysql.sync',
            'tsadm_cmd_args_encode': 'LS1kc3RfZW52PXJlZ3IuZGV2IC0tc3JjX2Vudj1yZWdyLnRlc3Q='
        }
        self.fail_reload = 3
        self.fail_reload_wait = 3
