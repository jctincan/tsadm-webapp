
ALTER TABLE `host` ADD COLUMN `ssh_key` blob NOT NULL;

UPDATE `tsadm` SET `dbversion` = 10000006;
