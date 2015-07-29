
from . import groupvars
from . import hostvars

wapp = None


def __init():
    groupvars.wapp = wapp
    hostvars.wapp = wapp


def getinv():
    __init()
    slave_all = wapp.db.slave_all()
    inv = {
        'all': {
            'hosts': [h['fqdn'] for h in slave_all],
            'vars': groupvars.hosts_all()
        },
        'master_server': {
            'hosts': [wapp.conf.get('MASTER_SERVER')],
            'vars': groupvars.master_server()
        },
        'slave_servers': {
            'hosts': [h['fqdn'] for h in slave_all],
            'vars': {}
        },
        '_meta': {
            'hostvars': hostvars.getall(slave_all),
        }
    }
    return inv
