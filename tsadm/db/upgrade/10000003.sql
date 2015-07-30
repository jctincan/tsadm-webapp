
ALTER TABLE `user` ADD COLUMN `last_seen` decimal(16, 6) unsigned NOT NULL DEFAULT 0.0;
UPDATE `tsadm` SET `dbversion` = 10000003;
