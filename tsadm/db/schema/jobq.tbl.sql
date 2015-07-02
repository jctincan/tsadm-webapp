-- $Id: jobq.tbl.sql 11812 2014-09-18 17:59:20Z jrms $

CREATE TABLE IF NOT EXISTS `jobq` (
    `id` char(41) NOT NULL DEFAULT '',
    `user_id` int(10) unsigned NOT NULL DEFAULT 0,
    `siteenv_id` int(10) unsigned NOT NULL DEFAULT 0,
    `cmd_name` varchar(64) NOT NULL DEFAULT '',
    `cmd_args` varchar(512) NOT NULL DEFAULT '',
    `cmd_exit` int(4) unsigned NOT NULL DEFAULT 9999,
    `cmd_output` mediumtext NOT NULL DEFAULT '',
    `tstamp_start` int(10) unsigned NOT NULL DEFAULT 0,
    `tstamp_end` int(10) unsigned NOT NULL DEFAULT 0,
    `status` varchar(5) NOT NULL DEFAULT '',
    `adm_log` binary(1) DEFAULT 0,
    PRIMARY KEY (`id`),
    KEY `user_id` (`user_id`),
    KEY `siteenv_id` (`siteenv_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
