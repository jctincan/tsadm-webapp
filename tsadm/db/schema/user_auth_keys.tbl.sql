DROP TABLE IF EXISTS `user_auth_keys`;
CREATE TABLE `user_auth_keys` (
    `user_id` int(10) unsigned NOT NULL,
    `ssh_key` blob NOT NULL,
    `key_bits` int(4) unsigned NOT NULL,
    `fingerprint` blob NOT NULL,
    `key_name` char(64) NOT NULL,
    `key_protocol` char(16) NOT NULL,
    UNIQUE KEY `fingerprint` (`fingerprint`(128)),
    UNIQUE KEY `ssh_key` (`ssh_key`(128)),
    KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
