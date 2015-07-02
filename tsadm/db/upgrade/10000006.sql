-- $Id: 10000006.sql 12828 2015-05-05 23:38:31Z jrms $

ALTER TABLE `host` ADD COLUMN `ssh_key` blob NOT NULL;

UPDATE `tsadm` SET `dbversion` = 10000006;
