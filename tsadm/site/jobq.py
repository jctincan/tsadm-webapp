# $Id: jobq.py 12179 2014-11-29 05:55:57Z jrms $

from tsadm.jobq.cmd import TSAdmJobQCmd


class EnvLiveSet(TSAdmJobQCmd):
    def __init__(self, *init_args):
        TSAdmJobQCmd.__init__(self, *init_args)

    def execute(self, args=''):
        jobq_id = self.jobq.start(self.name, args)
        self.db.env_live_set(self.env_id)
        self.jobq.end(jobq_id, 0, 'env live set')
        return jobq_id


class EnvLiveUnset(TSAdmJobQCmd):
    def __init__(self, *init_args):
        TSAdmJobQCmd.__init__(self, *init_args)

    def execute(self, args=''):
        jobq_id = self.jobq.start(self.name, args)
        self.db.env_live_unset(self.env_id)
        self.jobq.end(jobq_id, 0, 'env live unset')
        return jobq_id


ENV_CMD_MAP = {
    'env.live-set': EnvLiveSet,
    'env.live-unset': EnvLiveUnset,
}
