# $Id: intcmd.py 12179 2014-11-29 05:55:57Z jrms $

from tsadm.jobq.cmd import TSAdmJobQCmdInvoke
from tsadm.site.jobq import ENV_CMD_MAP


class TSAdmJobQIntCmdInvoke(TSAdmJobQCmdInvoke):
    __MAP = dict()
    def __init__(self, *init_args):
        self.__MAP.update(ENV_CMD_MAP)
        TSAdmJobQCmdInvoke.__init__(self, self.__MAP, *init_args)
