ALTER TABLE `user` ADD COLUMN `setenv_devel` binary(1) DEFAULT 0;
UPDATE `tsadm` SET `dbversion` = 10000008;
