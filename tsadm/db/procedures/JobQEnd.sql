-- $Id: JobQEnd.sql 11698 2014-09-03 22:55:50Z jrms $

DROP PROCEDURE IF EXISTS JobQEnd;

DELIMITER //
CREATE PROCEDURE JobQEnd(
    IN job_id char(41),
    IN tstamp int(10),
    IN cmd_exit int(4),
    IN cmd_output mediumtext)
BEGIN
    UPDATE `jobq`
        SET `tstamp_end` = tstamp,
            `cmd_exit` = cmd_exit,
            `cmd_output` = cmd_output,
            `status` = 'END'
        WHERE `id` = job_id;
    COMMIT;
END //
DELIMITER ;
