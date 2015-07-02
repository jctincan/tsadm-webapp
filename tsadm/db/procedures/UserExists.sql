-- $Id: UserExists.sql 11585 2014-07-31 03:12:19Z jrms $

DROP PROCEDURE IF EXISTS UserExists;

DELIMITER //
CREATE PROCEDURE UserExists(
    IN user_name varchar(64),
    OUT user_id int(10))
BEGIN
    SELECT `id`
        INTO user_id
        FROM `user`
        WHERE `name` = user_name
        LIMIT 1;
END //
DELIMITER ;
