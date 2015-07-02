-- $Id: SiteEnvGetId.sql 11585 2014-07-31 03:12:19Z jrms $

DROP PROCEDURE IF EXISTS SiteEnvGetId;

DELIMITER //
CREATE PROCEDURE SiteEnvGetId(
    IN site_name varchar(64),
    IN site_env varchar(16),
    OUT siteenv_id int(10))
BEGIN
    SELECT `siteenv`.`id` INTO siteenv_id
        FROM `siteenv` LEFT JOIN `site`
        ON `siteenv`.`site_id` = `site`.`id`
        WHERE `siteenv`.`name` = site_env AND `site`.`name` = site_name
        LIMIT 1;
END //
DELIMITER ;
