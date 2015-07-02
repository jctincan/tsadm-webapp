-- $Id: site.tbl.sql 12777 2015-04-10 22:24:35Z jrms $

CREATE TABLE IF NOT EXISTS `site` (
    `id` int(10) unsigned NOT NULL DEFAULT 0,
    `name` varchar(32) NOT NULL,
    `repo_uri` varchar(256) NOT NULL DEFAULT '__REPO_URI__',
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
