-- $Id: SiteEnvUnlock.sql 11585 2014-07-31 03:12:19Z jrms $

DROP PROCEDURE IF EXISTS SiteEnvUnlock;

DELIMITER //
CREATE PROCEDURE SiteEnvUnlock(
    IN siteenv_id int(10),
    IN jobr_id varchar(64),
    IN user_id int(10))
BEGIN
    UPDATE `siteenv`
        SET `lock` = 0
        WHERE `id` = siteenv_id
            AND `jobr_id` = jobr_id
            AND `lock_user_id` = user_id
            AND `lock` = 1;
    COMMIT;
END //
DELIMITER ;
