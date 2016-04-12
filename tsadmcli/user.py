import argparse

import tsadm.db
from tsadm import log

parser = argparse.ArgumentParser()
db = tsadm.db.TSAdmDB()


def list():
    for u in db.user_all():
        print(u['id'], u['name'], u['acclvl'], 'devel:'+u['setenv_devel'])
    return 0


def new():
    parser.add_argument('name', help="site name")
    args = parser.parse_args()
    db.user_add(args.name)
    log.inf('new user:', args.name)
    return 0


def remove():
    parser.add_argument('name', help="site name")
    args = parser.parse_args()
    uid = db.user_id(args.name)
    if uid == 0:
        print('ERROR: invalid user:', args.name)
        return 1
    db.user_remove(uid)
    log.inf('user removed:', uid, args.name)
    return 0
