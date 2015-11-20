import argparse

parser = argparse.ArgumentParser()
parser.add_argument('name', help="site name")

import tsadm.db
from tsadm import log

def new():
    args = parser.parse_args()
    db = tsadm.db.TSAdmDB()
    sid = db.site_id(args.name)
    if sid != 0:
        print("ERROR: a site called '{}' already exists: {}".format(args.name, sid))
        return 1
    db.site_add(args.name)
    log.inf("site '", args.name, "' was created")
    return 0
