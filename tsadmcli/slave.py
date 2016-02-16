import argparse

import tsadm.db
from tsadm import log

parser = argparse.ArgumentParser()
db = tsadm.db.TSAdmDB()

def list():
    for slv in db.slave_all():
        print(slv['id'], slv['fqdn'])
    return 0

def new():
    parser.add_argument('fqdn', help="host fqdn")
    args = parser.parse_args()
    for slv in db.slave_all():
        if slv['fqdn'] == args.fqdn:
            print("ERROR: slave already exists:", args.fqdn)
            return 1
    db.slave_add(args.fqdn)
    log.inf("new slave added: ", args.fqdn)
    return 0

def remove():
    parser.add_argument('fqdn', help="host fqdn")
    args = parser.parse_args()
    slave = None
    for slv in db.slave_all():
        if slv['fqdn'] == args.fqdn:
            slave = slv
            break
    if slave is None:
        print("ERROR: slave not found:", args.fqdn)
        return 1
    envs = db.slave_envs(slave['id'])
    if envs:
        print("ERROR: remove associated site envs first")
        return 2
    db.slave_remove(args.fqdn)
    log.inf("slave removed: ", args.fqdn)
    return 0
