ALTER TABLE `siteenv` ADD COLUMN `live` binary(1) DEFAULT '0';
UPDATE `siteenv` SET `live` = '1' WHERE `name` = 'prod';
UPDATE `tsadm` SET `dbversion` = 10000001;
