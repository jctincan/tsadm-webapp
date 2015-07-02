-- $Id: SiteEnvLockReq.sql 11585 2014-07-31 03:12:19Z jrms $

DROP PROCEDURE IF EXISTS SiteEnvLockReq;

DELIMITER //
CREATE PROCEDURE SiteEnvLockReq(
    IN siteenv_id int(10),
    IN jobr_id varchar(64),
    IN user_id int(10))
BEGIN
    UPDATE `siteenv`
        SET `jobr_id` = jobr_id,
            `lock_user_id` = user_id
        WHERE `id` = siteenv_id
            AND `lock` = 0;
    COMMIT;
END //
DELIMITER ;
