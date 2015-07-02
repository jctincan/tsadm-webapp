# $Id: jobq.py 12223 2014-12-01 21:11:11Z jrms $

from tsadm.jobq.cmd import TSAdmJobQCmd

RSYNC_CMD_MAP = {
    'rsync.dirs': TSAdmJobQCmd,
}

RSYNC_REQ_MAP = {
    'rsync.sources': TSAdmJobQCmd,
}
