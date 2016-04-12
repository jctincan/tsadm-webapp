import argparse

import tsadm.db
from tsadm import log

parser = argparse.ArgumentParser()
db = tsadm.db.TSAdmDB()

def list():
    for u in db.user_all():
        print(u['id'], u['name'], u['acclvl'], 'devel:'+u['setenv_devel'])
