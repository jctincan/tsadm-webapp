-- $Id: 10000003.sql 12593 2015-02-11 00:59:26Z jrms $

ALTER TABLE `user` ADD COLUMN `last_seen` decimal(16, 6) unsigned NOT NULL DEFAULT 0.0;
UPDATE `tsadm` SET `dbversion` = 10000003;
