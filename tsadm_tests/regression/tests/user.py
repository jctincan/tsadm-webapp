
from .. import RegressionTest

class RTUserName(RegressionTest):
    def configure(self):
        self.url = '/user/'
        self.check_regex = r'^.*Fingerprint:[^\d]+(44:30:B1:38:11:EE:02:03:95:A9:42:93:F8:E6:B0:AA:AC:A1:06:F3|84:AA:E1:F4:BF:BE:47:47:ED:75:07:F6:35:7A:ED:98:D0:85:90:23)$'
        self.fail_abort = True
