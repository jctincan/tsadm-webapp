ALTER TABLE `site` ADD COLUMN `parent_id` int(10) unsigned NOT NULL DEFAULT 0;
UPDATE `tsadm` SET `dbversion` = 10000009;
