# $Id: jobq.py 12180 2014-11-29 06:09:59Z jrms $

from tsadm.jobq.cmd import TSAdmJobQCmd

MYSQL_CMD_MAP = {
    'mysql.sync': TSAdmJobQCmd,
}
