-- $Id: SiteEnvUnlockReq.sql 11585 2014-07-31 03:12:19Z jrms $

DROP PROCEDURE IF EXISTS SiteEnvUnlockReq;

DELIMITER //
CREATE PROCEDURE SiteEnvUnlockReq(
    IN siteenv_id int(10),
    IN jobr_id varchar(64))
BEGIN
    UPDATE `siteenv`
        SET `jobr_id` = jobr_id
        WHERE `id` = siteenv_id
            AND `lock` = 1;
    COMMIT;
END //
DELIMITER ;
