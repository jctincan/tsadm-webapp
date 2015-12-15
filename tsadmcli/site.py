import argparse

import tsadm.db
from tsadm import log

parser = argparse.ArgumentParser()


def new():
    parser.add_argument('name', help="site name")
    args = parser.parse_args()
    db = tsadm.db.TSAdmDB()
    sid = db.site_id(args.name)
    if sid != 0:
        print("ERROR: a site called '{}' already exists: {}".format(args.name, sid))
        return 1
    db.site_add(args.name)
    log.inf("site '", args.name, "' was created")
    return 0


def list():
    db = tsadm.db.TSAdmDB()
    for sinfo in db.site_all():
        print(sinfo[0], sinfo[1])
    return 0
