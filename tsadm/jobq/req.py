
from tsadm.jobq.cmd import TSAdmJobQCmdInvoke
from tsadm.slave.jobq import SLAVE_REQ_MAP
from tsadm.git.jobq import GIT_REQ_MAP
from tsadm.rsync.jobq import RSYNC_REQ_MAP


class TSAdmJobQReqInvoke(TSAdmJobQCmdInvoke):
    __MAP = dict()
    def __init__(self, *init_args):
        self.__MAP.update(SLAVE_REQ_MAP)
        self.__MAP.update(GIT_REQ_MAP)
        self.__MAP.update(RSYNC_REQ_MAP)
        TSAdmJobQCmdInvoke.__init__(self, self.__MAP, *init_args)
