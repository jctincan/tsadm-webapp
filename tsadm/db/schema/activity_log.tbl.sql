DROP TABLE IF EXISTS `activity_log`;
CREATE TABLE `activity_log` (
    `tstamp` decimal(16,6) unsigned NOT NULL DEFAULT '0.000000',
    `took` varchar(16) NOT NULL DEFAULT '',
    `user_id` int(10) unsigned NOT NULL DEFAULT '0',
    `page_uri` varchar(256) NOT NULL DEFAULT '',
    KEY `tstamp` (`tstamp`),
    KEY `page_uri` (`page_uri`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
