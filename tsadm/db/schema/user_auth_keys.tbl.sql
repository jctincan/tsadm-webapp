CREATE TABLE IF NOT EXISTS `user_auth_keys` (
    `fingerprint` blob NOT NULL PRIMARY KEY,
    `ssh_key` blob NOT NULL UNIQUE KEY,
    `user_id` int(10) unsigned NOT NULL,
    `key_bits` int(4) unsigned NOT NULL,
    `key_name` char(64) NOT NULL,
    `key_protocol` char(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
