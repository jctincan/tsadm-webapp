import argparse

import tsadm.db
from tsadm import log

parser = argparse.ArgumentParser()
db = tsadm.db.TSAdmDB()

def list():
    for site in db.site_all():
        for senv in db.siteenv_all(site[0]):
            print(senv['id'], site[1], senv['name'])
