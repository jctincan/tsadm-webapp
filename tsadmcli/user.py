import argparse

import tsadm.db
from tsadm import log

parser = argparse.ArgumentParser()
db = tsadm.db.TSAdmDB()


def list():
    for u in db.user_all():
        print(u['id'], u['name'], u['acclvl'], 'devel:'+u['setenv_devel'])


def new():
    parser.add_argument('name', help="site name")
    args = parser.parse_args()
    db.user_add(args.name)
    log.inf('new user:', args.name)
