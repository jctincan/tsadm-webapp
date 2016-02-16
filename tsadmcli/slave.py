import argparse

import tsadm.db
from tsadm import log

parser = argparse.ArgumentParser()
db = tsadm.db.TSAdmDB()

def list():
    for slv in db.slave_all():
        print(slv['id'], slv['fqdn'])
    return 0
