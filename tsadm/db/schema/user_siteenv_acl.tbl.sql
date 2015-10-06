DROP TABLE IF EXISTS `user_siteenv_acl`;
CREATE TABLE `user_siteenv_acl` (
    `user_id` int(10) unsigned NOT NULL DEFAULT '0',
    `siteenv_id` int(10) unsigned NOT NULL DEFAULT '0',
    KEY `user_id` (`user_id`),
    KEY `siteenv_id` (`siteenv_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
