
import mysql.connector
import tsadm.db.config
import tsadm.log

from tsadm.db.sql import SQL, SP


class TSAdmDBVersionError(Exception):
    msg = None
    db_version = None

    def __init__(self, msg, version):
        self.msg = msg
        self.db_version = version


class TSAdmDB:
    DBVERSION = 10000010
    SITE_ID_MIN = 100
    SITEENV_ID_MIN = 5000

    __db = None
    __cursor = None
    __callsp_no = 0
    __exec_no = 0
    __exec2_no = 0
    version = None


    def __init__(self):
        config = tsadm.db.config.Config.dbinfo().copy()
        self.__db = mysql.connector.Connect(**config)
        self.__cursor = self.__db.cursor()
        tsadm.log.dbg('db: connect')
        #~ tsadm.log.dbg('db: ', dir(self.__db))
        #~ tsadm.log.dbg('cursor: ', dir(self.__cursor))
        if not self.__conn_check():
            raise Exception('database connection check failed')
        if not self.__dbversion_check():
            raise TSAdmDBVersionError('database version check failed', self.version)


    def __dbversion_check(self):
        cur_version = self.DBVERSION
        try:
            self.version = self.__exec(SQL.DBVERSION)[0][0]
        except:
            self.version = 0
        tsadm.log.dbg('dbversion cur: ', cur_version)
        tsadm.log.dbg('dbversion: ', self.version)
        return self.version == cur_version


    def __conn_check(self):
        return self.__db.cmd_ping()


    def __callsp(self, spcode, args):
        self.__callsp_no += 1
        try:
            r = self.__cursor.callproc(spcode, args)
        except Exception as e:
            tsadm.log.err('db_callsp: ', e)
            return None
        w = self.__cursor.fetchwarnings()
        if w is not None:
            tsadm.log.dbg('db_callsp warning: ', w)
        return r


    def __exec(self, sql, fetch_result=True):
        #~ sql_dbg = ''
        #~ for l in sql.split('\n'):
            #~ sql_dbg += l.strip() + ' '
        #~ tsadm.log.dbg('db.exec: ', sql_dbg)
        self.__cursor.execute(sql)
        w = self.__cursor.fetchwarnings()
        if w is not None:
            tsadm.log.dbg('db_exec warning: ', w)
        self.__exec_no += 1
        if fetch_result:
            return self.__cursor.fetchall()
        else:
            return self.__db.commit()


    def __exec2(self, sql, decode=True, exclude_columns=[]):
        self.__cursor.execute(sql)
        w = self.__cursor.fetchwarnings()
        if w is not None:
            tsadm.log.dbg('db_exec2 warning: ', w)
        self.__exec2_no += 1
        r = list()
        for row in self.__cursor.fetchall():
            d = dict()
            field_idx = 0
            for cname in self.__cursor.column_names:
                if cname not in exclude_columns:
                    if decode and type(row[field_idx]) is bytes:
                        d[cname] = row[field_idx].decode()
                    # FIXME: this is too ugly...
                    elif decode and repr(row[field_idx]).startswith('Decimal('):
                        d[cname] = float(row[field_idx])
                    else:
                        d[cname] = str(row[field_idx])
                field_idx += 1
            r.append(d)
        return r


    def close(self):
        self.__cursor.close()
        self.__db.disconnect()
        tsadm.log.dbg('db: disconnect')
        tsadm.log.dbg('db callsp: ', self.__callsp_no)
        tsadm.log.dbg('db exec: ', self.__exec_no)
        tsadm.log.dbg('db exec2: ', self.__exec2_no)


    def server_version(self):
        v = []
        for i in self.__db.get_server_version():
            v.append(str(i))
        return '.'.join(v)


    def conn_version(self):
        return mysql.connector.version.VERSION_TEXT


    def server_charset(self):
        return self.__db.charset


    def site_add(self, site_name, child_of):
        self.__exec(SQL.SITE_ADD.format(site_name, int(child_of)), fetch_result=False)


    def site_remove(self, site_id):
        self.__exec(SQL.SITE_REMOVE.format(site_id), fetch_result=False)


    def site_all(self):
        return self.__exec(SQL.SITE_ALL)


    def site_all2(self):
        sall = list()
        try:
            rows = self.__exec(SQL.SITE_ALL)
            for r in rows:
                sall.append({
                    'id': r[0],
                    'name': r[1],
                })
        except:
            pass
        return sall


    def site_id(self, site_name):
        try:
            r = int(self.__exec(SQL.SITE_ID.format(site_name))[0][0])
            return r
        except:
            return 0


    def site_info(self, site_id):
        try:
            return self.__exec2(SQL.SITE_INFO.format(site_id))[0]
        except IndexError:
            return {}


    def site_log(self, site_id):
        l = list()
        for r in self.__exec(SQL.SITE_LOG.format(site_id)):
            d = {
                'id': r[0],
                'user_name': r[1],
                'cmd_name': r[2],
                'cmd_exit': r[3],
                'tstamp_start': r[4],
                'tstamp_end': r[5],
                'status': r[6],
                'env_name': r[7]
            }
            l.append(d)
        return l


    def site_auth_users(self, site_id):
        return [str(k[0]) for k in self.__exec(SQL.SITE_AUTH_USERS.format(site_id=site_id))]


    def site_auth_hosts(self, site_id):
        return [str(k[0]) for k in self.__exec(SQL.SITE_AUTH_HOSTS.format(site_id=site_id))]


    def site_hosts(self, site_id):
        return [r[0] for r in self.__exec(SQL.SITE_HOSTS.format(site_id=site_id))]


    def site_envs_other(self, site_id, site_env, user_id):
        return [{'name': n[0], 'host': n[1]} for n in self.__exec(SQL.SITE_ENVS_OTHER.format(site_id, site_env, user_id, user_id))]


    def siteenv_add(self, site_name, env_name, host_fqdn):
        self.__exec(SQL.SITEENV_ADD.format(site_name, env_name, host_fqdn), fetch_result=False)


    def siteenv_all(self, site_id):
        rtrn = list()
        for r in self.__exec(SQL.SITEENV_ALL.format(site_id)):
            d = {
                'id': r[0],
                'name': r[1],
                'locked': int(r[2]),
                'claimed': int(r[3]),
                'live': int(r[6])
            }
            if d.get('locked'):
                d['locked_by'] = self.user_name(r[4])
            if d.get('claimed'):
                d['claimed_by'] = self.user_name(r[5])
            rtrn.append(d)
        tsadm.log.dbg('db.sitenv_all: rtrn=', rtrn)
        return rtrn


    def sites_envs_all(self):
        return [{'site_name': r[0], 'env_name': r[1], 'host_fqdn': r[2]} for r  in self.__exec(SQL.SITES_ENVS_ALL)]


    def user_exists(self, name):
        r = self.__callsp(SP.USER_EXISTS, (name, 0))
        return r[1]


    def user_siteenv_acl_remove(self, user_id):
        return self.__exec(SQL.USER_SITEENV_ACL_REMOVE.format(user_id), fetch_result=False)


    def user_remove(self, user_id):
        return self.__exec(SQL.USER_REMOVE.format(user_id), fetch_result=False)


    def user_siteenv_acl(self, user_id):
        return [a[0] for a in self.__exec(SQL.USER_SITEENV_ACL.format(user_id))]


    def user_siteenv_acl_set(self, user_id, env_id):
        return self.__exec(SQL.USER_SITEENV_ACL_SET.format(int(user_id), int(env_id)), fetch_result=False)


    def user_siteenv_acl_unset(self, user_id, env_id):
        return self.__exec(SQL.USER_SITEENV_ACL_UNSET.format(int(user_id), int(env_id)), fetch_result=False)


    def user_name(self, user_id):
        r = self.__exec(SQL.USER_NAME.format(user_id))
        try:
            return r[0][0]
        except:
            return 'NONE'


    def user_id(self, user_name):
        r = self.__exec(SQL.USER_ID.format(user_name))
        try:
            return int(r[0][0])
        except:
            return 0


    def user_acclvl(self, user_id):
        r = self.__exec(SQL.USER_ACCLVL.format(user_id))
        try:
            return r[0][0]
        except:
            return 'USER'


    def user_info(self, user_id):
        r = self.__exec2(SQL.USER_INFO.format(user_id), exclude_columns=['id', 'name', 'acclvl'])
        return r[0]


    def user_last_seen(self, user_id, tstamp):
        return self.__exec(SQL.USER_LAST_SEEN.format(int(tstamp), user_id), fetch_result=False)


    def user_all(self):
        return self.__exec2(SQL.USER_ALL)


    def user_add(self, name):
        return self.__exec(SQL.USER_ADD.format(name), fetch_result=False)


    def user_acclvl_set(self, uid, lvl):
        return self.__exec(SQL.USER_ACCLVL_SET.format(lvl, int(uid)), fetch_result=False)


    def user_devel_set(self, uid, devel):
        return self.__exec(SQL.USER_DEVEL_SET.format(int(devel), int(uid)), fetch_result=False)


    def user_disable(self, uid):
        return self.__exec(SQL.USER_DISABLE.format(int(uid)), fetch_result=False)


    def user_auth_keys(self, user_id):
        return [r[0].decode() for r in self.__exec(SQL.USER_AUTH_KEYS.format(user_id))]


    def user_auth_key_import(self, user_id, kname, kblob, kbits, kfprint, kprot):
        return self.__exec(SQL.USER_AUTH_KEY_IMPORT.format(
            user_id=user_id,
            ssh_key=kblob,
            key_bits=kbits,
            fingerprint=kfprint,
            key_name=kname,
            key_protocol=kprot,
        ), fetch_result=False)


    def user_auth_keys_full(self, user_id):
        return self.__exec2(SQL.USER_AUTH_KEYS_FULL.format(user_id))


    def user_auth_sites(self, user_id):
        rows = self.__exec(SQL.USER_AUTH_SITES.format(user_id))
        return [{'name': r[0], 'id': r[1]} for r in rows]


    def user_auth_getkey(self, user_id, kfprint):
        r = self.__exec2(SQL.USER_AUTH_GETKEY.format(user_id, kfprint))
        try:
            return r[0]
        except IndexError:
            return None


    def user_auth_delkey(self, user_id, kfprint):
        self.__exec(SQL.USER_AUTH_DELKEY.format(user_id, kfprint), fetch_result=False)


    def user_auth_siteenvs(self, user_id, site_id):
        return self.__exec(SQL.USER_AUTH_SITEENVS.format(user_id, site_id))


    def siteenv_id(self, sname, senv):
        r = self.__callsp(SP.SITEENV_ID, (sname, senv, 0))
        return r[2] or 0


    def siteenv_info(self, env_id):
        return self.__exec2(SQL.SITEENV_INFO.format(int(env_id)))[0]


    def siteenv_host(self, senv_id):
        q = SQL.SITEENV_HOST.format(senv_id)
        r = self.__exec(q)
        try:
            return (r[0][0], r[0][1])
        except Exception as e:
            return ('__NOT_SET__', 0)


    def siteenv_claim_req(self, jobr_id, user_id, siteenv_id):
        return self.__exec(SQL.SITEENV_CLAIM_REQ.format(jobr_id, user_id, siteenv_id), fetch_result=False)


    def siteenv_claim(self, siteenv_id, jobr_id, user_id):
        return self.__exec(SQL.SITEENV_CLAIM.format(siteenv_id, jobr_id, user_id), fetch_result=False)


    def siteenv_claim_info(self, siteenv_id):
        r = self.__exec(SQL.SITEENV_CLAIM_INFO.format(siteenv_id))
        try:
            d = {
                'claim': int(r[0][0]),
                'claim_by': r[0][1]
            }
        except:
            d = {
                'claim': 0,
                'claim_by': 0
            }
        return d


    def siteenv_release_req(self, jobr_id, user_id, siteenv_id):
        return self.__exec(SQL.SITEENV_RELEASE_REQ.format(jobr_id, user_id, siteenv_id), fetch_result=False)


    def siteenv_release(self, siteenv_id, jobr_id, user_id):
        return self.__exec(SQL.SITEENV_RELEASE.format(siteenv_id, jobr_id, user_id), fetch_result=False)


    def siteenv_remove(self, senv_id):
        self.__exec(SQL.SITEENV_REMOVE.format(senv_id), fetch_result=False)


    def siteenv_acl_remove(self, senv_id):
        self.__exec(SQL.SITEENV_ACL_REMOVE.format(senv_id), fetch_result=False)


    def siteenv_live(self, env_id):
        r = self.__exec(SQL.SITEENV_LIVE.format(env_id))
        try:
            return int(r[0][0])
        except:
            return 0


    def siteenv_lock_req(self, siteenv_id, jobr_id, user_id):
        return self.__callsp(SP.SITEENV_LOCK_REQ, (siteenv_id, jobr_id, user_id))


    def siteenv_lock(self, siteenv_id, jobr_id, user_id):
        return self.__callsp(SP.SITEENV_LOCK, (siteenv_id, jobr_id, user_id))


    def siteenv_lock_get(self, siteenv_id):
        r = self.__callsp(SP.SITEENV_LOCK_GET, (siteenv_id, b'0', 0, ''))
        tsadm.log.dbg('lock r1: ', r[1])
        if r[1] is None:
            l = 0
        else:
            l = int(r[1])
        return (l, r[2], r[3])


    def siteenv_unlock_req(self, siteenv_id, jobr_id):
        return self.__callsp(SP.SITEENV_UNLOCK_REQ, (siteenv_id, jobr_id))


    def siteenv_unlock(self, siteenv_id, jobr_id, user_id):
        return self.__callsp(SP.SITEENV_UNLOCK, (siteenv_id, jobr_id, user_id))


    def siteenv_site_name(self, senv_id):
        r = self.__exec(SQL.SITEENV_SITE_NAME.format(senv_id))
        try:
            return r[0][0]
        except:
            return 'ERROR'


    def siteenv_name(self, senv_id):
        r = self.__exec(SQL.SITEENV_NAME.format(senv_id))
        try:
            return r[0][0]
        except:
            return 'ERROR'


    def jobq_start(self, job_id, user_id, se_id, cmd_name, cmd_args, tstamp, adm_log):
        if adm_log:
            adm_log = b'1'
        else:
            adm_log = b'0'
        return self.__callsp(SP.JOBQ_START, (job_id, user_id, se_id, cmd_name, cmd_args, tstamp, adm_log))


    def jobq_end(self, job_id, tstamp, cmd_exit, cmd_output):
        return self.__callsp(SP.JOBQ_END, (job_id, tstamp, cmd_exit, cmd_output))


    def jobq_status_update(self, job_id, status):
        return self.__exec(SQL.JOBQ_STATUS_UPDATE.format(status, job_id), fetch_result=False)


    def jobq_senv_all(self, senv_id):
        # jrms
        rtrn = list()
        rows = self.__exec(SQL.JOBQ_SENV_ALL.format(senv_id))
        for r in rows:
            ed = dict()
            ed['id'] = r[0]
            ed['user'] = r[1]
            ed['cmd_name'] = r[2]
            ed['cmd_exit'] = r[3]
            ed['tstamp_start'] = r[4]
            ed['tstamp_end'] = r[5]
            ed['status'] = r[6]
            rtrn.append(ed)
        return rtrn


    def jobq_server(self, senv_id):
        r = self.__exec(SQL.JOBQ_SERVER.format(senv_id))
        tsadm.log.dbg('db.jobq_server: ', r)
        try:
            return r[0][0]
        except IndexError:
            return '__NOT_SET__'


    def jobq_get(self, job_id):
        dbr = self.__exec(SQL.JOBQ_GET.format(job_id))
        try:
            r = dbr[0]
            d = {
                'id': r[0],
                'cmd_name': r[1],
                'cmd_args': r[2],
                'status': r[3],
                'senv': r[4],
                'sname': r[5],
            }
            return d
        except Exception as e:
            tsadm.log.err('db.jobq_get: ', e)
            return None


    def jobq_get_info(self, senv_id, job_id):
        sql_query = SQL.JOBQ_GET_INFO.format(senv_id, job_id)
        #~ tsadm.log.dbg('db.jobq_get_info query: ', sql_query)
        dbr = self.__exec(sql_query)
        try:
            r = dbr[0]
            d = {
                'id': r[0],
                'cmd_name': r[1],
                'cmd_args': r[2],
                'cmd_rtrn': r[3],
                'cmd_output': r[4],
                'status': r[5],
                'tstamp_start': r[6],
                'tstamp_end': r[7],
                'user_name': r[8],
                'senv': r[9],
                'sname': r[10]
            }
            return d
        except Exception as e:
            #~ tsadm.log.dbg('db.jobq_get_info query: ', sql_query)
            tsadm.log.dbg('db.jobq_get_info dbr: ', dbr)
            tsadm.log.err('db.jobq_get_info: ', e)
            return None


    def jobq_maint(self, days_max=120):
        return self.__exec(SQL.JOBQ_MAINT.format(days_max), fetch_result=False)


    def adm_log(self):
        l = list()
        for r in self.__exec(SQL.ADM_LOG):
            d = {
                'id': r[0],
                'user_name': r[1],
                'cmd_name': r[2],
                'cmd_exit': r[3],
                'tstamp_start': r[4],
                'tstamp_end': r[5],
                'status': r[6],
                'site_name': r[7],
                'env_name': r[8]
            }
            l.append(d)
        return l


    def slave_add(self, fqdn):
        self.__exec(SQL.SLAVE_ADD.format(fqdn), fetch_result=False)


    def slave_all(self):
        r = self.__exec(SQL.SLAVE_ALL)
        sall = list()
        try:
            for s in r:
                sall.append({
                    'id': s[0],
                    'fqdn': s[1]
                })
        except:
            pass
        return sall


    def slave_envs(self, host_id):
        return self.__exec(SQL.SLAVE_ENVS.format(host_id))


    def slave_id(self, slave_slug):
        r = self.__exec(SQL.SLAVE_ID.format(slave_slug))
        try:
            return r[0][0]
        except:
            return None


    def slave_info(self, slave_id):
        r = self.__exec(SQL.SLAVE_INFO.format(slave_id))
        try:
            return {
                'fqdn': r[0][0],
                'slug': r[0][1],
            }
        except:
            return {}


    def slave_sites(self, slave_id):
        return self.__exec(SQL.SLAVE_SITES.format(slave_id))


    def slave_remove(self, fqdn):
        self.__exec(SQL.SLAVE_REMOVE.format(fqdn), fetch_result=False)

    def env_live_set(self, env_id):
        return self.__exec(SQL.ENV_LIVE_SET.format(env_id), fetch_result=False)


    def env_live_unset(self, env_id):
        return self.__exec(SQL.ENV_LIVE_UNSET.format(env_id), fetch_result=False)


    def activity_log_put(self, tstamp, took_s, user_id, page_uri):
        return self.__exec(SQL.ACTIVITY_LOG_PUT.format(int(tstamp), took_s, user_id, page_uri), fetch_result=False)


    def activity_log_get(self, limit=50):
        l = list()
        r = self.__exec(SQL.ACTIVITY_LOG_GET.format(limit))
        for row in r:
            d = {
                'tstamp': float(row[0]),
                'took': row[1],
                'user_name': row[2],
                'page_uri': row[3][:24],
            }
            l.append(d)
        return l


    def activity_log_maint(self, days_max=30):
        return self.__exec(SQL.ACTIVITY_LOG_MAINT.format(days_max), fetch_result=False)


    def asbinv_developers(self):
        rows = self.__exec(SQL.ASBINV_DEVELOPERS)
        return rows
        #~ rtrn = dict()
        #~ for r in rows:
            #~ site_id = r[0]
            #~ rtrn[site_id] = {
                #~ 'name': r[1],
            #~ }
        #~ return rtrn


    def asbinv_sites(self):
        rows = self.__exec(SQL.ASBINV_SITES)
        rtrn = dict()
        for r in rows:
            site_id = r[0]
            rtrn[site_id] = {
                'name': r[1],
                'repo_uri': r[2]
            }
        return rtrn


    def asbinv_siteenvs(self):
        rows = self.__exec(SQL.ASBINV_SITEENVS)
        rtrn = dict()
        for r in rows:
            envid = r[0]
            rtrn[envid] = {
                'site_name': r[1],
                'name': r[2],
                'host_id': str(r[3]),
                'site_repo_uri': r[4],
                'site_id': str(r[5]),
                'id': str(r[6]),
                'live': r[7].decode(),
                'site_parent_id': str(r[8]),
            }
        return rtrn


    def asbinv_slave_sites(self, host_id):
        return [{"id": r[0], "name": r[1]} for r in self.__exec(SQL.ASBINV_SLAVE_SITES.format(host_id=host_id))]


    def asbinv_slave_siteenvs(self, slave_id):
        return [str(r[0]) for r in self.__exec(SQL.ASBINV_SLAVE_SITEENVS.format(slave_id))]


    def asbinv_dump_table(self, tname, unique_key='id', limit=1000, exclude_columns=[]):
        sql_query = SQL.ASBINV_DUMP_TABLE.format(tname=tname, limit=limit)
        if unique_key is None:
            return self.__exec2(sql_query, exclude_columns=exclude_columns)
        else:
            d = dict()
            for r in self.__exec2(sql_query, exclude_columns=exclude_columns):
                r_id = r[unique_key]
                d[r_id] = r
            return d


    def asbinv_master_developers(self):
        return self.__exec2(SQL.ASBINV_MASTER_DEVELOPERS)
