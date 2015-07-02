-- $Id: 10000005.sql 12777 2015-04-10 22:24:35Z jrms $

ALTER TABLE `site` ADD COLUMN `repo_uri` varchar(256) NOT NULL DEFAULT '__REPO_URI__';
ALTER TABLE `host` ADD COLUMN `www_port` int(5) unsigned NOT NULL DEFAULT 80;
UPDATE `tsadm` SET `dbversion` = 10000005;
