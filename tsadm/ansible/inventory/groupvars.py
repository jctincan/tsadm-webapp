class G:
    all_siteenv = None
    all_user = None
    all_site = None
    all_user_siteenv_acl = None
    sites_all = None
    tsadm_developers = None

wapp = None


def __developer_sites_envs_auth(user_id):
    auth_sites = wapp.db.user_auth_sites(user_id)
    sites_auth = list()
    envs_auth = list()
    for site in auth_sites:
        sites_auth.append(str(site['id']))
        rows = wapp.db.user_auth_siteenvs(user_id, site['id'])
        envs_auth.extend([str(r[0]) for r in rows])
    return (sites_auth, envs_auth)


def __tsadm_developers():
    rows = wapp.db.asbinv_developers()
    wapp.log.dbg('tsadm_developers: ', rows)
    rtrn = dict()
    for r in rows:
        user_id = r[0]
        if user_id not in rtrn.keys():
            rtrn[user_id] = {
                'name': r[1],
                'auth_keys': list()
            }
        auth_key = r[2].decode()
        rtrn[user_id]['auth_keys'].append(auth_key)
        sites_auth, envs_auth = __developer_sites_envs_auth(user_id)
        rtrn[user_id]['sites_auth'] = sites_auth
        rtrn[user_id]['envs_auth'] = envs_auth
    G.tsadm_developers = rtrn
    return rtrn


def __all_host():
    # TODO: agregar la pub ssh key del server (tsadm@server:~/.ssh/id_*.pub)
    return wapp.db.asbinv_dump_table('host', limit=50)


def __all_siteenv():
    envs = wapp.db.asbinv_siteenvs()
    for eid in envs.keys():
        site_name = envs[eid]['site_name']
        env_name = envs[eid]['name']
        envs[eid]['slug'] = wapp.slug(site_name, env_name)
        # site repo uri
        repo_uri = envs[eid]['site_repo_uri']
        if repo_uri == '' or repo_uri == '__REPO_URI__':
            # if repo uri isn't saved in the database, use the config
            # template to generate it
            envs[eid]['site_repo_uri'] = wapp.conf.get('SITE_REPO_URI_TMPL').format(user=wapp.slug(site_name), repo=site_name)
    return envs


def __all_user_siteenv_acl():
    if G.all_user_siteenv_acl is None:
        rtrn = dict()
        rows = wapp.db.asbinv_dump_table('user_siteenv_acl', unique_key=None)
        for r in rows:
            user_id = r['user_id']
            if user_id not in rtrn.keys():
                rtrn[user_id] = {'siteenv_ids': list()}
            siteenv_id = r['siteenv_id']
            if int(siteenv_id) == 0:
                rtrn[user_id]['siteenv_ids'] = [str(k) for k in __all_siteenv().keys()]
            else:
                rtrn[user_id]['siteenv_ids'].append(str(siteenv_id))
        G.all_user_siteenv_acl = rtrn
    return G.all_user_siteenv_acl


def __all_user_auth_keys():
    rtrn = dict()
    rows = wapp.db.asbinv_dump_table('user_auth_keys', unique_key=None, limit=150)
    for r in rows:
        user_id = r['user_id']
        if user_id not in rtrn.keys():
            rtrn[user_id] = {'auth_keys': list()}
        rtrn[user_id]['auth_keys'].append(r['ssh_key'])
    return rtrn


def __all_user():
    if G.all_user is None:
        G.all_user = wapp.db.asbinv_dump_table('user', limit=50, exclude_columns=['last_seen', 'acclvl'])
        for uid in G.all_user.keys():
            user_name = G.all_user[uid]['name']
            G.all_user[uid]['slug'] = wapp.slug(user_name)
    return G.all_user


def __all_site():
    if G.all_site is None:
        G.all_site = wapp.db.asbinv_dump_table('site', limit=200)
    for site_id in G.all_site.keys():
        site_name = G.all_site[site_id]['name']
        G.all_site[site_id]['slug'] = wapp.slug(site_name)
    return G.all_site


def __all_site_auth():
    sites = __all_site()
    rtrn = dict()
    for site_id in sites.keys():
        if site_id not in rtrn.keys():
            rtrn[site_id] = {
                'site_id': site_id,
                'auth_users': __site_auth_users(site_id),
                'auth_hosts': __site_auth_hosts(site_id),
            }
    return rtrn


def hosts_all():
    return {
        'tsadmdb_host': __all_host(),
        'tsadmdb_user': __all_user(),
        'tsadmdb_user_siteenv_acl': __all_user_siteenv_acl(),
        'tsadmdb_siteenv': __all_siteenv(),
        'tsadmdb_site': __all_site(),
        'tsadmdb_user_auth_keys': __all_user_auth_keys(),
        'tsadm_site_auth': __all_site_auth(),
    }


def __master_developers():
    return [str(d['id']) for d in wapp.db.asbinv_master_developers()]


def __site_auth_hosts(site_id):
    return wapp.db.site_auth_hosts(site_id)


def __site_auth_users(site_id):
    return wapp.db.site_auth_users(site_id)


def master_server():
    return {
        'tsadm_developers': __master_developers(),
    }
