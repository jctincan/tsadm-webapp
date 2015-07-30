
DROP PROCEDURE IF EXISTS SiteEnvLock;

DELIMITER //
CREATE PROCEDURE SiteEnvLock(
    IN siteenv_id int(10),
    IN jobr_id varchar(64),
    IN user_id int(10))
BEGIN
    UPDATE `siteenv`
        SET `lock` = 1
        WHERE `id` = siteenv_id
            AND `jobr_id` = jobr_id
            AND `lock_user_id` = user_id
            AND `lock` = 0;
    COMMIT;
END //
DELIMITER ;
