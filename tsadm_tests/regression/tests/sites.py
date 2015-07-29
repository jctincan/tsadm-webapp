
from .. import RegressionTest


class RTSiteEnv(RegressionTest):
    def configure(self):
        self.url = '/'
        #~ self.check_regex = r'.*<b>test:</b> <a href="/site/regr/test/">regr\.test</a>$'
        self.fail_abort = True
        self.check_digest = '6b7964193bb2ab040961c26b2dbc4698dcbe6f7a'


class RTSiteEnvClaim(RegressionTest):
    def configure(self):
        self.url = '/site/regr/test/claim/'
        self.check_regex = r'^.*\s<a href="/site/regr/test/release/">env.release</a>'
        self.fail_abort = True

    def pre_run(self):
        clines = self.get_content()
        confirm_id = self.line_regex_get(clines, r'.*href="/site/regr/test/claim/([a-f0-9]+)/">claim\.confirm.*', 1)
        if confirm_id is not None:
            self.url += confirm_id + '/'


class RTSiteEnvRelease(RegressionTest):
    def configure(self):
        self.url = '/site/regr/test/release/'
        self.check_regex = r'^.*\s<a href="/site/regr/test/claim/" [^>]+>env.claim</a>'

    def pre_run(self):
        clines = self.get_content()
        confirm_id = self.line_regex_get(clines, r'.*href="/site/regr/test/release/([a-f0-9]+)/">release\.confirm.*', 1)
        if confirm_id is not None:
            self.url += confirm_id + '/'


class RTSiteEnvLock(RegressionTest):
    def configure(self):
        self.url = '/site/regr/test/lock/'
        self.check_regex = r'^<p><a href="/site/regr/test/unlock/">env\.unlock</a></p>$'
        self.fail_abort = True

    def pre_run(self):
        clines = self.get_content()
        confirm_id = self.line_regex_get(clines, r'.*href="/site/regr/test/lock/([a-f0-9]+)/">lock\.confirm.*', 1)
        if confirm_id is not None:
            self.url += confirm_id + '/'


class RTSiteEnvUnlock(RegressionTest):
    def configure(self):
        self.url = '/site/regr/test/unlock/'
        self.check_regex = r'^.*\s<a href="/site/regr/test/lock/" [^>]+>env\.lock</a>'

    def pre_run(self):
        clines = self.get_content()
        confirm_id = self.line_regex_get(clines, r'.*href="/site/regr/test/unlock/([a-f0-9]+)/">unlock\.confirm.*', 1)
        if confirm_id is not None:
            self.url += confirm_id + '/'


class RTSiteEnvLiveSet(RegressionTest):
    def configure(self):
        self.url = '/jobq/ice/regr/test/env.live-set/'
        self.check_regex = r'^env live set$'


class RTSiteEnvLiveUnset(RegressionTest):
    def configure(self):
        self.url = '/jobq/ice/regr/test/env.live-unset/'
        self.check_regex = r'^env live unset$'


class RTSiteLog(RegressionTest):
    def configure(self):
        self.url = '/'
        self.check_regex = r'^<!-- CMD_STATUS=env\.live-unset:0 -->$'

    def pre_run(self):
        self.url = self.get_prev_url()
