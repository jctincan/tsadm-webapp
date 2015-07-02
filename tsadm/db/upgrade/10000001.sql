-- $Id: 10000001.sql 12116 2014-11-19 15:51:01Z jrms $
ALTER TABLE `siteenv` ADD COLUMN `live` binary(1) DEFAULT '0';
UPDATE `siteenv` SET `live` = '1' WHERE `name` = 'prod';
UPDATE `tsadm` SET `dbversion` = 10000001;
