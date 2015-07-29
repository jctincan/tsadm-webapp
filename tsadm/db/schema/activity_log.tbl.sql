
CREATE TABLE IF NOT EXISTS `activity_log` (
    `tstamp` decimal(16, 6) unsigned NOT NULL DEFAULT 0,
    `took` varchar(16) NOT NULL DEFAULT '',
    `user_id` int(10) unsigned NOT NULL DEFAULT 0,
    `page_uri` varchar(256) NOT NULL DEFAULT '',
    KEY (`tstamp`),
    KEY (`page_uri`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
