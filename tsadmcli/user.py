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
    parser.add_argument('name', help="user name")
    args = parser.parse_args()
    db.user_add(args.name)
    log.inf('new user:', args.name)
    return 0


def remove():
    parser.add_argument('name', help="user name")
    args = parser.parse_args()
    uid = db.user_id(args.name)
    if uid == 0:
        print('ERROR: invalid user:', args.name)
        return 1
    db.user_remove(uid)
    log.inf('user removed:', uid, args.name)
    return 0


def __user_enable(uid, name):
    db.user_acclvl_set(uid, 'USER')
    log.inf('user enabled:', uid, name)
    return 0


def __user_disable(uid, name):
    db.user_acclvl_set(uid, 'DISABLE')
    log.inf('user disabled:', uid, name)
    return 0


def __user_devel_setup(uid, name, devel):
    if devel == 'on':
        db.user_devel_set(uid, 1)
        log.inf('user devel setup:', uid, name, devel)
        return 0
    elif devel == 'off':
        db.user_devel_set(uid, 0)
        log.inf('user devel setup:', uid, name, devel)
        return 0
    else:
        print('ERROR: invalid argument:', devel)
        return 3


def modify():
    parser.add_argument('--enable', action='store_true', help="enable user")
    parser.add_argument('--disable', action='store_true', help="disable user")
    parser.add_argument('--devel', choices=['on', 'off'], help="enable/disable devel setup")
    parser.add_argument('name', help="user name")
    args = parser.parse_args()
    uid = db.user_id(args.name)
    if uid == 0:
        print('ERROR: invalid user:', args.name)
        return 1
    if args.enable:
        return __user_enable(uid, args.name)
    elif args.disable:
        return __user_disable(uid, args.name)
    elif args.devel:
        return __user_devel_setup(uid, args.name, args.devel)
    else:
        print('\nERROR: one of --enable|--disable|--devel arguments must be present\n')
        parser.print_help()
        return 2
    return 0
