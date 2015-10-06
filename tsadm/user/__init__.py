import re
import time
import tempfile
import subprocess

from datetime import datetime


re_cert_email = re.compile(r'^([\w.]+)@tsadm\.tincan\.co\.uk$')
re_auth_key_name = re.compile(r'^[a-zA-Z0-9@\.-]+$')

USER_ACCLVL = {
    'DISABLE':    999,
    'ADMIN':      910,
    'SITE_ADMIN': 905,
    'ADMIN_LOW':  900,
    'BOT':        810,
    'HOST':       800,
    'USER':       100,
    'NOACCESS':     0,
}


class TSAdmUser:
    _log = None
    _db = None
    _cert_data = None
    _cert_email = None
    _cert_fingerprint = None
    _cert_since = None
    _cert_until = None
    _conf = None
    _umesg = None
    id = None
    name = None
    siteenv_acl = None
    acclvl = None


    def __init__(self, log, db, conf, umesg):
        self._log = log
        self._db = db
        self.acclvl = 'NOACCESS'
        self._conf = conf
        self._umesg = umesg


    def auth_check(self, cert_data):
        self._cert_data = cert_data
        self._log.dbg('cert_data: ', cert_data)
        self._cert_email = cert_data[0].strip()
        if not re_cert_email.match(self._cert_email):
            self._log.err('user bad cert email: ' + repr(self._cert_email))
            return False
        self.name = self._cert_email.replace('@tsadm.tincan.co.uk', '')
        self.id = self._db.user_exists(self.name)
        if self.id is None or self.id <= 0:
            self._log.err('user not found: ', self.name, ' ', self.id)
            return False
        return True


    def load(self):
        self._cert_fingerprint = self._cert_data[1].strip().split('=')[1]
        self._cert_since = self._cert_data[2].strip().split('=')[1]
        self._cert_until = self._cert_data[3].strip().split('=')[1]

        self.siteenv_acl = self._db.user_siteenv_acl(self.id)
        self.acclvl = self._db.user_acclvl(self.id)

        cert_until_tstamp = datetime.strptime(self._cert_until, self._conf.get('USER_CERT_DATE_FMT')).timestamp()
        cert_valid_for = cert_until_tstamp - time.time()
        if cert_valid_for <= (3600*24*15):
            self._umesg.warn('your personal certificate is about to expire!')

        self._log.inf('user loaded: ', self.name)
        self._log.dbg('user id: ', self.id)
        self._log.dbg('siteenv acl: ', self.siteenv_acl)
        self._log.dbg('user acclvl: ', self.acclvl)
        self._log.dbg('user cert valid for: ', cert_valid_for)
        return True


    def acclvl_check(self, check_level):
        if self.acclvl not in USER_ACCLVL:
            self._log.err('user_acclvl wrong: ', self.acclvl)
            return 'WRONG'
        if self.acclvl == 'DISABLE':
            self._log.err('user_acclvl user disable: ', self.acclvl)
            return 'USER_DISABLE'
        if check_level not in USER_ACCLVL:
            self._log.err('user_acclvl check wrong: ', check_level)
            return 'CHECK_WRONG'
        if check_level == 'DISABLE':
            self._log.err('user_acclvl page disable: ', check_level)
            return 'PAGE_DISABLE'
        user_acclvl_no = USER_ACCLVL.get(self.acclvl)
        check_level_no = USER_ACCLVL.get(check_level)
        if user_acclvl_no < check_level_no:
            self._log.err('user_acclvl low: ', self.acclvl)
            return 'LOW'
        self._log.inf('user access level OK: ', self.acclvl)
        return 'OK'


    def tmpl_data(self):
        d = {
            'id': self.id,
            'name': self.name,
            'cert': {
                'fingerprint': self._cert_fingerprint,
                'since': self._cert_since,
                'until': self._cert_until,
            },
            'is_admin': False,
            'acclvl': self.acclvl.lower(),
            'is_site_admin': False,
            'auth_keys': self._db.user_auth_keys_full(self.id),
        }
        if USER_ACCLVL.get(self.acclvl) == USER_ACCLVL.get('ADMIN'):
            d['is_admin'] = True
        if USER_ACCLVL.get(self.acclvl) >= USER_ACCLVL.get('SITE_ADMIN'):
            d['is_site_admin'] = True
        if self.id is not None:
            d.update(self._db.user_info(self.id))
            d['last_seen'] = time.strftime(self._conf.get('CUR_TIME_FMT'), time.localtime(d['last_seen']))
        return d


    def _ssh_key_info(self, kname, key_text):
        # FIXME
        kblob = ' '.join(key_text.split()[:-1])
        kblob += ' '+kname
        kbits = None
        kfprint = None
        ktype = None

        self._log.dbg('import key blob: ', kblob)

        with tempfile.NamedTemporaryFile(mode='w+') as fh:
            fh.write(kblob)
            fh.flush()
            fh.seek(0, 0)

            try:
                ssh_info = subprocess.check_output([self._conf.get('SSH_KEYGEN'), '-l', '-f', fh.name])
            except Exception as e:
                self._log.dbg(repr(e))
                raise RuntimeError(e.output.decode())

            fh.close()

        ssh_info_items = ssh_info.strip().split()
        kbits = ssh_info_items[0].decode()
        kfprint = ssh_info_items[1].decode()
        ktype = ssh_info_items[3].decode().replace('(', '').replace(')', '')

        self._log.dbg('user auth kname: ', kname, ' - kbits: ', kbits, ' - kfprint: ', kfprint, ' - ktype: ', ktype)
        return (kname, kblob, kbits, kfprint, ktype)


    def auth_key_import(self, key_name, key_text):
        if not re_auth_key_name.match(key_name):
            return (False, 'invalid key name')
        self._db.user_auth_key_import(self.id, *self._ssh_key_info(key_name, key_text))
        return (True, '')
