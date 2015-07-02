-- $Id: SiteEnvLockGet.sql 11585 2014-07-31 03:12:19Z jrms $

DROP PROCEDURE IF EXISTS SiteEnvLockGet;

DELIMITER //
CREATE PROCEDURE SiteEnvLockGet(
    IN siteenv_id int(10),
    OUT locked binary(1),
    OUT locked_by_id int(10),
    OUT locked_by_name varchar(64))
BEGIN
    SELECT `siteenv`.`lock`,
            `siteenv`.`lock_user_id`
        INTO locked,
            locked_by_id
        FROM `siteenv`
        WHERE `siteenv`.`id` = siteenv_id
        LIMIT 1;

    SELECT `user`.`name`
        INTO locked_by_name
        FROM `user`
        WHERE `user`.`id` = locked_by_id
        LIMIT 1;
END //
DELIMITER ;
