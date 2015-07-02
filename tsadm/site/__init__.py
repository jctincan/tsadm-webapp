# $Id: __init__.py 12569 2015-02-05 17:42:43Z jrms $

class TSAdmSiteEnv:
    _log = None
    _db = None
    _user = None
    _conf = None
    _site_name = None
    id = None
    name = None
    host = None
    host_id = None
    host_slug = None
    locked = None
    locked_by = None
    claimed = None
    claim_ok = None
    claimed_by = None
    is_live = None


    def __init__(self, log, db, user, conf):
        self._log = log
        self._db = db
        self._user = user
        self._conf = conf


    def load(self, site_name, env_name):
        self._site_name = site_name
        self.name = env_name
        self.id = self._db.siteenv_id(site_name, self.name)
        if self.id == 0 and not self.name.startswith('__'):
            self._log.err('site env not found')
            return False
        self.host, self.host_slug = self._db.siteenv_host(self.id)
        self.is_live = self._db.siteenv_live(self.id)
        return True


    def acl_check(self):
        if self._site_name.startswith('__') and self.name.startswith('__'):
            self._log.dbg('site.env.acl_check: {} page - authorizing...'.format(self._site_name))
            return True
        if self.id not in self._user.siteenv_acl:
            if 0 in self._user.siteenv_acl:
                # Grant access to any site env
                self._log.inf('user access to ANY site env')
                return True
            else:
                self._log.err('site.env.acl_check: unauthorized')
                return False
        self._log.dbg('site.env.acl_check: OK')
        return True


    def lock_check(self, unlock_req):
        self.locked = False
        if unlock_req:
            self.locked = True
            self._log.inf('site.env.lock: unlock request')
            return (False, 0, '')
        locked, locked_by_id, locked_by_name = self._db.siteenv_lock_get(self.id)
        self._log.inf('site.env.lock: ', locked)
        self._log.dbg('site.env.lock locked_by_id: ', locked_by_id)
        self._log.dbg('site.env.lock locked_by_name: ', locked_by_name)
        if locked:
            self.locked = True
            self.locked_by = locked_by_name
            err_code = 901
            err_msg = 'site env locked'
            if locked_by_id != self._user.id:
                # only the same user that locked it can unlock a site env
                self._log.wrn('user can not unlock!')
                err_code = 902
                err_msg = 'can not unlock!!'
            return (True, err_code, err_msg)
        return (False, 0, '')


    def claim_check(self):
        self._log.dbg('site.env.claim_check')
        self.claimed = False
        self.claim_ok = True
        self.claimed_by = 'NONE'
        claim_info = self._db.siteenv_claim_info(self.id)
        self.claimed = claim_info.get('claim', 0)
        self._log.dbg('site.env.claim_check claimed: ', self.claimed)
        if self.claimed:
            claim_by = claim_info.get('claim_by', 0)
            self.claimed_by = self._db.user_name(claim_by)
            self._log.inf('site.env.claim_check claimed by: ', self.claimed_by)
            if claim_by != self._user.id:
                self.claim_ok = False
                return False
        self._log.dbg('claim OK')
        return True


    def tmpl_data(self):
        d = {
            'name': self.name,
            'locked_by': self.locked_by,
            'host': self.host,
            'host_slug': self.host_slug,
            'domain': self._conf.get('SITE_ENV_DOMAIN', 'tsadm.local'),
            'claimed': self.claimed,
            'claimed_by': self.claimed_by,
            'live': self.is_live,
        }
        if self.locked_by == self._user.name:
            d['locked_by'] == 'you'
        if self.claimed_by == self._user.name:
            d['claimed_by'] == 'you'
        return d


class TSAdmSite:
    _log = None
    _db = None
    _user = None
    id = None
    name = None
    env = None
    envs_other = None


    def __init__(self, log, db, user, conf):
        self._log = log
        self._db = db
        self._user = user
        self.env = TSAdmSiteEnv(log, db, user, conf)


    def load(self, site_name, env_name):
        self.name = site_name
        self.id = self._db.site_id(self.name)
        if not self.env.load(site_name, env_name):
            return False
        self._log.dbg('site.env.id: ', self.env.id)
        self.envs_other = self._db.site_envs_other(self.id, self.env.name, self._user.id)
        self._log.dbg('envs_other: ', self.envs_other)
        self._log.inf('{}.{} loaded'.format(self.name, self.env.name))
        return True


    def tmpl_data(self):
        d = {
            'load_navbar': False
        }
        if not self.name.startswith('__'):
            d = {
                'load_navbar': True,
                'name': self.name,
                'envs_other': self.envs_other,
                'env': self.env.tmpl_data(),
            }
        if not self.env.claim_ok:
            d['load_navbar'] = False
        if self.env.locked:
            d['load_navbar'] = False
        return d


def envs_all(wapp):
    envs_all = list()
    sites_all = wapp.db.site_all2()
    envs_all.append({
        'id': '__ALL_ALL__',
        'slug': 'ALL.ALL',
    })
    for s in sites_all:
        envs_all.append({
            'id': '__ALL_SITE:{}'.format(s['name']),
            'slug': '{}.ALL'.format(s['name']),
        })
        site_envs = wapp.db.siteenv_all(s['id'])
        for se in site_envs:
            envs_all.append({
                'id': se['id'],
                'slug': '{}.{}'.format(s['name'], se['name']),
            })
    return envs_all
