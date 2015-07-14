-- $Id: host.tbl.sql 12828 2015-05-05 23:38:31Z jrms $

CREATE TABLE IF NOT EXISTS `host` (
  `id` int(10) unsigned NOT NULL DEFAULT 0,
  `fqdn` varchar(128) NOT NULL DEFAULT '__HOST_FQDN__',
  `www_port` int(5) unsigned NOT NULL DEFAULT 80,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fqdn` (`fqdn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
