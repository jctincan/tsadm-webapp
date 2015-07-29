
from . import groupvars
from . import hostvars

wapp = None


def __init():
    groupvars.wapp = wapp
    hostvars.wapp = wapp


def getinv():
    __init()
    master_server = wapp.conf.get('MASTER_SERVER')
    slave_all = wapp.db.slave_all()
    hosts_all = [h['fqdn'] for h in slave_all]
    hosts_all.append(master_server)
    inv = {
        'all': {
            'hosts': hosts_all,
            'vars': groupvars.hosts_all()
        },
        'master_server': {
            'hosts': [master_server],
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
