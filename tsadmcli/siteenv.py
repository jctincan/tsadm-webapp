import argparse

import tsadm.db
from tsadm import log

parser = argparse.ArgumentParser()
db = tsadm.db.TSAdmDB()

def list():
    for site in db.site_all():
        for senv in db.siteenv_all(site[0]):
            print(senv['id'], site[1], senv['name'])

def new():
    parser.add_argument('site', help="site name")
    parser.add_argument('env', help="env name")
    parser.add_argument('host', help="host fqdn")
    args = parser.parse_args()
    sid = db.site_id(args.site)
    if sid == 0:
        print("ERROR: site does not exists:", args.site)
        return 1
    for senv in db.siteenv_all(sid):
        if senv['name'] == args.env:
            print("ERROR: site env already exists:", args.env)
            return 2
    slave = None
    for slv in db.slave_all():
        if slv['fqdn'] == args.host:
            slave = slv
            break
    if slave is None:
        print("ERROR: host not found:", args.host)
        return 3
    db.siteenv_add(args.site, args.env, args.host)
    log.inf("site env created: {} {} {}".format(args.site, args.env, args.host))
    return 0

def remove():
    parser.add_argument('site', help="site name")
    parser.add_argument('env', help="env name")
    args = parser.parse_args()
    env_id = db.siteenv_id(args.site, args.env)
    if env_id == 0:
        print("ERROR: site env not found:", args.site, args.env)
        return 1
    db.siteenv_acl_remove(env_id)
    db.siteenv_remove(env_id)
    log.inf("site env removed: {} {} {}".format(env_id, args.site, args.env))
    return 0
