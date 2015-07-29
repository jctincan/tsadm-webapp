
CREATE TABLE IF NOT EXISTS `user_auth_keys` (
    `id` int(10) unsigned NOT NULL DEFAULT 0,
    `user_id` int(10) unsigned NOT NULL,
    `ssh_key` blob NOT NULL,
    PRIMARY KEY (`id`),
    KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
