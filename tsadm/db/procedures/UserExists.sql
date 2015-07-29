
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
