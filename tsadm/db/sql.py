class SP:
    SITEENV_ID = 'SiteEnvGetId'
    SITEENV_LOCK = 'SiteEnvLock'
    SITEENV_LOCK_REQ = 'SiteEnvLockReq'
    SITEENV_LOCK_GET = 'SiteEnvLockGet'
    SITEENV_UNLOCK = 'SiteEnvUnlock'
    SITEENV_UNLOCK_REQ = 'SiteEnvUnlockReq'
    JOBQ_START = 'JobQStart'
    JOBQ_END = 'JobQEnd'
    USER_EXISTS = 'UserExists'


class SQL:
    SITE_ADD = """
    INSERT INTO `site` (`id`, `name`)
        SELECT MAX(`id`)+1, '{}'
            FROM `site`
    """

    SITE_REMOVE = """
    DELETE FROM `site`
        WHERE `id` = {}
        LIMIT 1
    """

    SITE_ALL = """
    SELECT `id`, `name`
        FROM `site`
        ORDER BY `name`
        LIMIT 500
    """

    SITE_ID = """
    SELECT `id`
        FROM `site`
        WHERE `name` = '{}'
        LIMIT 1
    """

    SITE_LOG = """
    SELECT `jobq`.`id`,
            `user`.`name`,
            `jobq`.`cmd_name`,
            `jobq`.`cmd_exit`,
            `jobq`.`tstamp_start`,
            `jobq`.`tstamp_end`,
            `jobq`.`status`,
            `siteenv`.`name`
        FROM `jobq`
        LEFT JOIN (`user`, `siteenv`)
            ON `jobq`.`user_id` = `user`.`id`
            AND `jobq`.`siteenv_id` = `siteenv`.`id`
        WHERE `siteenv`.`site_id` = {}
        ORDER BY `jobq`.`tstamp_start` DESC
        LIMIT 75
    """

    SITE_AUTH_USERS = """
    SELECT DISTINCT `user_siteenv_acl`.`user_id`
    FROM (`site`, `siteenv`, `user_siteenv_acl`, `user_auth_keys`)
    WHERE `site`.`id` = {site_id} AND
        `siteenv`.`site_id` = `site`.`id` AND (
            `user_siteenv_acl`.`siteenv_id` = `siteenv`.`id` OR
            `user_siteenv_acl`.`siteenv_id` = 0
        ) AND
        `user_auth_keys`.`user_id` = `user_siteenv_acl`.`user_id`
    LIMIT 500
    """

    SITE_AUTH_HOSTS = """
    SELECT DISTINCT `host`.`id`
    FROM (`siteenv`, `host`)
    WHERE `siteenv`.`site_id` = {site_id}
        AND `siteenv`.`host_id` = `host`.`id`
    LIMIT 100
    """

    SITE_HOSTS = """
    SELECT DISTINCT `host`.`fqdn`
    FROM (`siteenv`, `host`)
    WHERE `siteenv`.`host_id` = `host`.`id` AND
        `siteenv`.`site_id` = {site_id}
    LIMIT 10
    """

    SITE_ENVS_OTHER = """
    SELECT `siteenv`.`name`,
            `host`.`fqdn`
        FROM `siteenv`
        LEFT JOIN (`user_siteenv_acl`, `host`)
            ON (
                (
                    `user_siteenv_acl`.`siteenv_id` = `siteenv`.`id`
                    OR `user_siteenv_acl`.`siteenv_id` = 0
                )
                AND `host`.`id` = `siteenv`.`host_id`
                )
        WHERE `siteenv`.`site_id` = {}
            AND `siteenv`.`name` != '{}'
            AND `user_siteenv_acl`.`user_id` = {}
            AND `siteenv`.`lock` = 0
            AND (`siteenv`.`claim` = 0 OR `siteenv`.`claim_user_id` = {})
            AND `siteenv`.`live` = 0
        LIMIT 50
    """

    SITES_ENVS_ALL = """
    SELECT `site`.`name`,
            `siteenv`.`name`,
            `host`.`fqdn`
        FROM (`siteenv`, `site`, `host`)
        LIMIT 1000
    """

    SITEENV_ALL = """
    SELECT `siteenv`.`id`,
            `siteenv`.`name`,
            `siteenv`.`lock`,
            `siteenv`.`claim`,
            `siteenv`.`lock_user_id`,
            `siteenv`.`claim_user_id`,
            `siteenv`.`live`
        FROM `siteenv`
        WHERE `siteenv`.`site_id` = {}
        LIMIT 500
    """

    SITEENV_HOST = """
    SELECT `host`.`fqdn`,
            CRC32(`host`.`fqdn`)
        FROM `host`
        LEFT JOIN `siteenv`
            ON `siteenv`.`host_id` = `host`.`id`
        WHERE `siteenv`.`id` = {}
        LIMIT 1
    """

    SITEENV_CLAIM_REQ = """
    UPDATE `siteenv`
        SET `jobr_id` = '{}',
            `claim_user_id` = {}
        WHERE `id` = {}
            AND `claim` = 0
    """

    SITEENV_CLAIM = """
    UPDATE `siteenv`
        SET `claim` = 1
        WHERE `id` = {}
            AND `jobr_id` = '{}'
            AND `claim_user_id` = {}
            AND `claim` = 0
    """

    SITEENV_CLAIM_INFO = """
    SELECT `claim`, `claim_user_id`
        FROM `siteenv`
        WHERE `id` = {}
        LIMIT 1
    """

    SITEENV_LIVE = """
    SELECT `live`
        FROM `siteenv`
        WHERE `id` = {}
        LIMIT 1
    """

    SITEENV_RELEASE_REQ = """
    UPDATE `siteenv`
        SET `jobr_id` = '{}'
        WHERE `claim_user_id` = {}
            AND `id` = {}
            AND `claim` = 1
    """

    SITEENV_RELEASE = """
    UPDATE `siteenv`
        SET `claim` = 0
        WHERE `id` = {}
            AND `jobr_id` = '{}'
            AND `claim_user_id` = {}
            AND `claim` = 1
    """

    SITEENV_SITE_NAME = """
    SELECT `site`.`name`
        FROM `siteenv`
            LEFT JOIN `site`
            ON `siteenv`.`site_id` = `site`.`id`
        WHERE `siteenv`.`id` = {}
        LIMIT 1
    """

    SITEENV_NAME = """
    SELECT `name`
        FROM `siteenv`
        WHERE `id` = {}
        LIMIT 1
    """

    USER_SITEENV_ACL = """
    SELECT `siteenv_id`
        FROM `user_siteenv_acl`
        WHERE `user_id` = {}
        LIMIT 500
    """

    USER_ACCLVL = """
    SELECT `acclvl`
        FROM `user`
        WHERE `id` = {}
        LIMIT 1
    """

    USER_NAME = """
    SELECT `name`
        FROM `user`
        WHERE `id` = {}
        LIMIT 1
    """

    USER_INFO = """
    SELECT *
        FROM `user`
        WHERE `id` = {}
        LIMIT 1
    """

    USER_LAST_SEEN = """
    UPDATE `user`
        SET `last_seen` = {}
        WHERE `id` = {}
    """

    USER_ALL = """
    SELECT *
        FROM `user`
        ORDER BY `name` ASC
        LIMIT 100
    """

    USER_AUTH_SITES = """
    SELECT DISTINCT `site`.`name`,
                    `site`.`id`
        FROM (`site`, `siteenv`, `user_siteenv_acl`)
        WHERE `user_siteenv_acl`.`user_id` = {} AND
            `user_siteenv_acl`.`user_id` >= 100 AND
            `siteenv`.`site_id` = `site`.`id` AND (
                `user_siteenv_acl`.`siteenv_id` = `siteenv`.`id` OR
                `user_siteenv_acl`.`siteenv_id` = 0
            )
        LIMIT 200
    """

    USER_AUTH_SITEENVS = """
    SELECT `siteenv`.`id`, `siteenv`.`name`, `host`.`fqdn`
        FROM (`siteenv`, `host`, `user_siteenv_acl`)
        WHERE `user_siteenv_acl`.`user_id` = {} AND
            `user_siteenv_acl`.`user_id` >= 100 AND
            `siteenv`.`site_id` = {}
        LIMIT 600
    """

    USER_AUTH_GETKEY = """
    SELECT *
        FROM `user_auth_keys`
        WHERE `user_id` = {}
        AND `fingerprint` = '{}'
        LIMIT 1
    """

    USER_AUTH_DELKEY = """
    DELETE FROM `user_auth_keys`
    WHERE `user_id` = {}
    AND `fingerprint` = '{}'
    """

    USER_AUTH_KEYS = """
    SELECT `ssh_key`
        FROM `user_auth_keys`
        WHERE `user_id` = {}
        LIMIT 20
    """

    USER_AUTH_KEY_IMPORT = """
    INSERT INTO `user_auth_keys`
    VALUES ({user_id},
        '{ssh_key}',
        {key_bits},
        '{fingerprint}',
        '{key_name}',
        '{key_protocol}')
    """

    USER_AUTH_KEYS_FULL = """
    SELECT *
    FROM `user_auth_keys`
    WHERE `user_id` = {}
    LIMIT 20
    """

    JOBQ_SENV_ALL = """
    SELECT `jobq`.`id`,
            `user`.`name`,
            `jobq`.`cmd_name`,
            `jobq`.`cmd_exit`,
            `jobq`.`tstamp_start`,
            `jobq`.`tstamp_end`,
            `jobq`.`status`
        FROM `jobq`
        LEFT JOIN `user`
            ON `jobq`.`user_id` = `user`.`id`
        WHERE `jobq`.`siteenv_id` = {}
        ORDER BY `jobq`.`tstamp_start` DESC
        LIMIT 25
    """

    JOBQ_SERVER = """
    SELECT `host`.`fqdn`
        FROM `host`
            LEFT JOIN `siteenv`
            ON `siteenv`.`host_id` = `host`.`id`
        WHERE `siteenv`.`id` = {}
        LIMIT 1
    """

    JOBQ_GET = """
    SELECT `jobq`.`id`,
            `jobq`.`cmd_name`,
            `jobq`.`cmd_args`,
            `jobq`.`status`,
            `siteenv`.`name` AS `senv`,
            `site`.`name` AS `sname`
        FROM `jobq`
        LEFT JOIN (`siteenv`, `site`)
            ON (
                `siteenv`.`id` = `jobq`.`siteenv_id` AND
                `site`.`id` = `siteenv`.`site_id`
            )
        WHERE `jobq`.`id` = '{}' AND
            `jobq`.`status` = 'START'
        LIMIT 1
    """

    JOBQ_STATUS_UPDATE = """
    UPDATE `jobq`
        SET `status` = '{}',
            `cmd_exit` = 9090
        WHERE `id` = '{}'
        AND `status` != 'END'
    """

    JOBQ_GET_INFO = """
    SELECT `jobq`.`id`,
            `jobq`.`cmd_name`,
            `jobq`.`cmd_args`,
            `jobq`.`cmd_exit`,
            `jobq`.`cmd_output`,
            `jobq`.`status`,
            `jobq`.`tstamp_start`,
            `jobq`.`tstamp_end`,
            `user`.`name` AS `user_name`,
            `siteenv`.`name` AS `senv`,
            `site`.`name` AS `sname`
        FROM `jobq`
        LEFT JOIN (`user`, `siteenv`, `site`)
            ON (
                `user`.`id` = `jobq`.`user_id` AND
                `siteenv`.`id` = `jobq`.`siteenv_id` AND
                `site`.`id` = `siteenv`.`site_id`
            )
        WHERE `jobq`.`siteenv_id` = {} AND
            `jobq`.`id` = '{}'
        LIMIT 1
    """

    JOBQ_MAINT = """
    DELETE FROM `jobq`
        WHERE TIMESTAMPDIFF(DAY, FROM_UNIXTIME(`tstamp_start`), NOW()) > {}
    """

    ADM_LOG = """
    SELECT `jobq`.`id`,
            `user`.`name`,
            `jobq`.`cmd_name`,
            `jobq`.`cmd_exit`,
            `jobq`.`tstamp_start`,
            `jobq`.`tstamp_end`,
            `jobq`.`status`,
            `site`.`name`,
            `siteenv`.`name`
        FROM `jobq`
        LEFT JOIN (`user`, `siteenv`, `site`)
            ON `jobq`.`user_id` = `user`.`id`
            AND `jobq`.`siteenv_id` = `siteenv`.`id`
            AND `siteenv`.`site_id` = `site`.`id`
        WHERE `jobq`.`adm_log` = 1
        ORDER BY `jobq`.`tstamp_start` DESC
        LIMIT 75
    """

    DBVERSION = """
    SELECT `dbversion`
        FROM `tsadm`
        LIMIT 1
    """

    SLAVE_ID = """
    SELECT `id`
        FROM `host`
        WHERE CRC32(`fqdn`) = {}
        LIMIT 1
    """

    SLAVE_INFO = """
    SELECT `fqdn`,
            CRC32(`fqdn`)
        FROM `host`
        WHERE `id` = {}
    """

    SLAVE_ALL = """
    SELECT `id`,
            `fqdn`
        FROM `host`
        ORDER BY `fqdn`
        LIMIT 200
    """

    SLAVE_SITES = """
    SELECT DISTINCT
            `site`.`id`,
            `site`.`name`
        FROM `site`
            LEFT JOIN (`siteenv`, `host`)
            ON (
                `siteenv`.`host_id` = `host`.`id` AND
                `siteenv`.`site_id` = `site`.`id`
            )
        WHERE `host`.`id` = '{}'
        LIMIT 200
    """

    ENV_LIVE_SET = """
    UPDATE `siteenv`
        SET `live` = '1'
        WHERE `id` = {}
    """

    ENV_LIVE_UNSET = """
    UPDATE `siteenv`
        SET `live` = '0'
        WHERE `id` = {}
    """

    ACTIVITY_LOG_PUT = """
    INSERT INTO `activity_log`
        VALUES ({}, '{}', {}, '{}')
    """

    ACTIVITY_LOG_GET = """
    SELECT `activity_log`.`tstamp`,
            `activity_log`.`took`,
            `user`.`name`,
            `activity_log`.`page_uri`
        FROM `activity_log`
        LEFT JOIN (`user`)
            ON `activity_log`.`user_id` = `user`.`id`
        WHERE `activity_log`.`page_uri` != '/admin/activity/'
        ORDER BY `tstamp` DESC
        LIMIT {}
    """

    ACTIVITY_LOG_MAINT = """
    DELETE FROM `activity_log`
        WHERE TIMESTAMPDIFF(DAY, FROM_UNIXTIME(`tstamp`), NOW()) > {}
    """

    ASBINV_DEVELOPERS = """
    SELECT `user`.`id`,
        `user`.`name`,
        `user_auth_keys`.`ssh_key`,
        `user`.`setenv_devel`
    FROM (`user`, `user_auth_keys`)
    WHERE `user`.`id` > 99
        AND `user`.`id` = `user_auth_keys`.`user_id`
    ORDER BY `user`.`id` ASC
    LIMIT 50
    """

    ASBINV_SITES = """
    SELECT `site`.`id`,
        `site`.`name`,
        `site`.`repo_uri`
    FROM `site`
    ORDER BY `site`.`id` ASC
    LIMIT 200
    """

    ASBINV_SITEENVS = """
    SELECT `siteenv`.`id`,
        `site`.`name`,
        `siteenv`.`name`,
        `host`.`id`,
        `site`.`repo_uri`,
        `site`.`id`,
        `siteenv`.`id`,
        `siteenv`.`live`,
        `site`.`parent_id`
    FROM (`siteenv`, `site`, `host`)
    WHERE `siteenv`.`site_id` = `site`.`id`
    ORDER BY `site`.`id`
    LIMIT 600
    """

    ASBINV_SLAVE_SITES = """
    SELECT DISTINCT
        `site`.`id`,
        `site`.`name`
    FROM `site`
        LEFT JOIN (`siteenv`, `host`)
        ON (
            `siteenv`.`host_id` = `host`.`id` AND
            `siteenv`.`site_id` = `site`.`id`
        )
    WHERE `host`.`id` = '{host_id}'
    ORDER BY `site`.`id` ASC
    LIMIT 200
    """

    ASBINV_SLAVE_SITEENVS = """
    SELECT DISTINCT
            `siteenv`.`id`
        FROM `site`
            LEFT JOIN (`siteenv`, `host`)
            ON (
                `siteenv`.`host_id` = `host`.`id` AND
                `siteenv`.`site_id` = `site`.`id`
            )
        WHERE `host`.`id` = '{}'
        LIMIT 600
    """

    ASBINV_DUMP_TABLE = 'SELECT * FROM `{tname}` LIMIT {limit}'

    ASBINV_MASTER_DEVELOPERS = 'SELECT `id` FROM `user` WHERE `id` > 99 LIMIT 50'
