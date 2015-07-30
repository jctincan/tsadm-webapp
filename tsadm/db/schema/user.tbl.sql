
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(10) unsigned NOT NULL DEFAULT 0,
  `name` varchar(64) NOT NULL,
  `acclvl` varchar(64) NOT NULL DEFAULT 'USER',
  `last_seen` decimal(16, 6) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
