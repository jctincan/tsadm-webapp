
from tsadm.jobq.cmd import TSAdmJobQCmdInvoke
from tsadm.site.jobq import ENV_CMD_MAP


class TSAdmJobQIntCmdInvoke(TSAdmJobQCmdInvoke):
    __MAP = dict()
    def __init__(self, *init_args):
        self.__MAP.update(ENV_CMD_MAP)
        TSAdmJobQCmdInvoke.__init__(self, self.__MAP, *init_args)
