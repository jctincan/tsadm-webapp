
wapp = None


def __slave_sites(server):
    return [str(site['id']) for site in wapp.db.asbinv_slave_sites(server['id'])]


def __getvars(server):
    return {
        'tsadm_slave_sites': __slave_sites(server),
        'tsadm_slave_siteenvs': wapp.db.asbinv_slave_siteenvs(server['id']),
    }


def getall(servers):
    hv = dict()
    for s in servers:
        host_fqdn = s['fqdn']
        hv[host_fqdn] = __getvars(s)
    return hv
