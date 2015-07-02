# $Id: jobq.py 12389 2015-01-15 03:37:42Z jrms $

from tsadm.jobq.cmd import TSAdmJobQCmd


class GitCmdFG(TSAdmJobQCmd):
    def __init__(self, *init_args):
        TSAdmJobQCmd.__init__(self, *init_args)
        self.runbg = False


class GitCmdBG(TSAdmJobQCmd):
    def __init__(self, *init_args):
        TSAdmJobQCmd.__init__(self, *init_args)
        self.runbg = True


GIT_CMD_MAP = {
    'git.log': (GitCmdFG, {'desc': 'Get the latest (15) log entries'}),
    'git.status': (GitCmdFG, {'desc': 'Get current status'}),
    'git.pull': (GitCmdBG, {'desc': 'Update current branch'}),
    'git.fetch': (GitCmdBG, {'desc': 'Fetch metadata'}),
    'git.checkout-tag': (GitCmdBG, {'show': False}),
    'git.checkout-branch': (GitCmdBG, {'show': False}),
    'git.cleanup': (GitCmdBG, {'desc': 'Discard any local change'}),
}

GIT_REQ_MAP = {
    'git.tags': GitCmdBG,
    'git.branches': GitCmdBG,
    'git.url': GitCmdBG,
    'git.branch': GitCmdBG,
}
