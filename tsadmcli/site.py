import argparse

import tsadm.db
from tsadm import log

parser = argparse.ArgumentParser()
db = tsadm.db.TSAdmDB()


def new():
    parser.add_argument('name', help="site name")
    parser.add_argument('--child-of', metavar='parent_name', help="name of the parent site", default="")
    args = parser.parse_args()
    sid = db.site_id(args.name)
    if sid != 0:
        print("ERROR: a site called '{}' already exists: {}".format(args.name, sid))
        return 1
    parent_id = 0
    if args.child_of != "":
        parent_id = db.site_id(args.child_of)
        if parent_id == 0:
            print("ERROR: parent site not found:", args.child_of)
            return 2
    db.site_add(args.name, parent_id)
    log.inf("site '", args.name, "' was created")
    return 0


def list():
    for sinfo in db.site_all():
        print(sinfo[0], sinfo[1])
    return 0


def remove():
    parser.add_argument('name', help="site name")
    args = parser.parse_args()
    site_id = db.site_id(args.name)
    if site_id == 0:
        print("ERROR: site does not exists: {}".format(args.name))
        return 1
    site_envs = db.siteenv_all(site_id)
    if site_envs:
        print("ERROR: remove associated environments first!")
        return 2
    # TODO: check if it has child sites before to remove
    db.site_remove(site_id)
    log.inf("site removed: {} {}".format(site_id, args.name))
    return 0
