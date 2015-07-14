ALTER TABLE `host` DROP COLUMN `ssh_key`;
UPDATE `tsadm` SET `dbversion` = 10000007;
