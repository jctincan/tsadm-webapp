# $Id: config.py 12271 2014-12-09 19:54:54Z jrms $

from . import user
from . import sites
from . import slave
from . import git
from . import jobq
from . import rsync
from . import mysql


LOAD_TESTS = {
    '000-user-name': user.RTUserName,
    '001-site-env': sites.RTSiteEnv,
    '002-slave': slave.RTSlave,
    '003-git-url': git.RTGitURL,
    '004-git-branch': git.RTGitBranch,
    '005-rsync': rsync.RTRsync,
    '006-jobq-cc': jobq.RTJobQCommandConfirm,

    '100-site-env-claim': sites.RTSiteEnvClaim,
    '101-site-env-release': sites.RTSiteEnvRelease,
    '102-site-env-lock': sites.RTSiteEnvLock,
    '103-site-env-unlock': sites.RTSiteEnvUnlock,
    '104-site-env-live-set': sites.RTSiteEnvLiveSet,
    '105-site-env-live-unset': sites.RTSiteEnvLiveUnset,
    '106-site-log': sites.RTSiteLog,

    '200-git-log': git.RTGitLog,
    '201-git-status': git.RTGitStatus,
    '210-git-pull': git.RTGitPull,
    '220-git-checkout-tag': git.RTGitCOTag,
    '230-git-checkout-branch': git.RTGitCOBranch,
    '240-git-cleanup': git.RTGitCleanup,
    '300-git-hook-post-receive': git.RTGitHookPostReceive,

    '400-rsync-dirs': rsync.RTRsyncDirs,

    '500-mysql-sync': mysql.RTMySQLSync,
}
