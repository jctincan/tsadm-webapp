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
