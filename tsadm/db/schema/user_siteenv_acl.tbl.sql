-- $Id: user_siteenv_acl.tbl.sql 11585 2014-07-31 03:12:19Z jrms $
CREATE TABLE IF NOT EXISTS `user_siteenv_acl` (
  `user_id` int(10) unsigned NOT NULL DEFAULT 0,
  `siteenv_id` int(10) unsigned NOT NULL DEFAULT 0,
  KEY `user_id` (`user_id`),
  KEY `siteenv_id` (`siteenv_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
