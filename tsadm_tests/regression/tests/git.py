# $Id: git.py 12759 2015-04-07 20:28:23Z jrms $

import time
from .. import RegressionTest


# URL: <span class="git-url">ssh://regr@tsadm.chroot:22/~/regr.git</span><br>
class RTGitURL(RegressionTest):
    def configure(self):
        self.url = '/git/regr/test/'
        #~ self.check_regex = r'^[\s]+URL:[^>]+href="/home/tsadm/sites/regr/r\.git">'
        self.check_regex = r'^[\s]+URL:[^>]+ssh://regr@.*\.git'
        self.fail_abort = True


class RTGitBranch(RegressionTest):
    def configure(self):
        self.url = '/git/regr/test/'
        self.check_regex = r'^[\s]+Server running: <b>regrtest</b>$'
        self.fail_abort = True


class RTGitLog(RegressionTest):
    def configure(self):
        self.url = '/jobq/ce/regr/test/'
        self.check_regex = r'^commit 6b8f9b917dcc246790d7580dc87ace5464583d0c$'
        self.post_data = {'tsadm_cmd': 'git.log'}


class RTGitStatus(RegressionTest):
    def configure(self):
        self.url = '/jobq/ce/regr/test/'
        self.check_regex = r'^nothing to commit \(working directory clean\)$'
        self.post_data = {'tsadm_cmd': 'git.status'}


class RTGitPull(RegressionTest):
    def configure(self):
        self.url = '/jobq/ce/regr/test/'
        self.check_regex = r'^<!-- CMD_STATUS=git\.pull:0 -->$'
        self.post_data = {'tsadm_cmd': 'git.pull'}
        self.fail_reload = 3
        self.fail_reload_wait = 2


class RTGitCOTag(RegressionTest):
    def configure(self):
        self.url = '/jobq/ce/regr/test/'
        self.check_regex = r'^<!-- CMD_STATUS=git\.checkout-tag:0 -->$'
        self.post_data = {
            'tsadm_cmd': 'git.checkout-tag',
            'tsadm_cmd_args_encode': 'LS1naXRfdGFnPXRhZzE='
        }
        self.fail_reload = 3
        self.fail_reload_wait = 2


class RTGitCOBranch(RegressionTest):
    def configure(self):
        self.url = '/jobq/ce/regr/test/'
        self.check_regex = r'^<!-- CMD_STATUS=git\.checkout-branch:0 -->$'
        self.post_data = {
            'tsadm_cmd': 'git.checkout-branch',
            'tsadm_cmd_args_encode': 'LS1naXRfYnJhbmNoPXJlZ3J0ZXN0'
        }
        self.fail_reload = 3
        self.fail_reload_wait = 2


class RTGitCleanup(RegressionTest):
    def configure(self):
        self.url = '/jobq/ce/regr/test/'
        self.check_regex = r'^<!-- CMD_STATUS=git\.cleanup:0 -->$'
        self.post_data = {'tsadm_cmd': 'git.cleanup'}
        self.fail_reload = 3
        self.fail_reload_wait = 2


class RTGitHookPostReceive(RegressionTest):
    def configure(self):
        self.url = '/git/hook/post-receive/'
        self.check_regex = r'^:-\) :-\)$'
        self.post_data = {'tsadm_post_data': 'NjkxYmYyNDgzNjk4OGUyNWYzYTJjODg1YTUxY2FjNWY3M2Q1Y2NlYQpyZWdyCnJlZ3J0ZXN0Cg=='}
