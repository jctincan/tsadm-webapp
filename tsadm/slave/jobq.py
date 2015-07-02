# $Id: jobq.py 12271 2014-12-09 19:54:54Z jrms $

from tsadm.jobq.cmd import TSAdmJobQCmd


class SlaveLoadAvg(TSAdmJobQCmd):
    def __init__(self, *init_args):
        TSAdmJobQCmd.__init__(self, *init_args)


SLAVE_REQ_MAP = {
    'slave.loadavg': SlaveLoadAvg,
    'slave.hostinfo': SlaveLoadAvg,
    'slave.softinfo': SlaveLoadAvg,
}
