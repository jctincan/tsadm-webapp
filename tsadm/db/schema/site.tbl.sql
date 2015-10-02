CREATE TABLE IF NOT EXISTS `site` (
    `id` int(10) unsigned NOT NULL DEFAULT 0,
    `name` varchar(32) NOT NULL,
    `repo_uri` varchar(256) NOT NULL DEFAULT '__REPO_URI__',
    `parent_id` int(10) unsigned NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
