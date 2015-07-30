
from tsadm.jobq.cmd import TSAdmJobQCmd


class SlaveLoadAvg(TSAdmJobQCmd):
    def __init__(self, *init_args):
        TSAdmJobQCmd.__init__(self, *init_args)


SLAVE_REQ_MAP = {
    'slave.loadavg': SlaveLoadAvg,
    'slave.hostinfo': SlaveLoadAvg,
    'slave.softinfo': SlaveLoadAvg,
}
