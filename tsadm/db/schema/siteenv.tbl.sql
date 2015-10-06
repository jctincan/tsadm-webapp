DROP TABLE IF EXISTS `siteenv`;
CREATE TABLE `siteenv` (
    `id` int(10) unsigned NOT NULL DEFAULT '0',
    `site_id` int(10) unsigned NOT NULL DEFAULT '0',
    `name` varchar(32) NOT NULL DEFAULT '',
    `jobr_id` varchar(64) NOT NULL DEFAULT '',
    `lock` binary(1) NOT NULL DEFAULT '0',
    `lock_user_id` int(10) unsigned NOT NULL DEFAULT '0',
    `claim` binary(1) NOT NULL DEFAULT '0',
    `claim_user_id` int(10) unsigned NOT NULL DEFAULT '0',
    `host_id` int(10) unsigned NOT NULL DEFAULT '0',
    `live` binary(1) DEFAULT '0',
    PRIMARY KEY (`id`),
    KEY `site_id` (`site_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
