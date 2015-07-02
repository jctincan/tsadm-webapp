-- $Id: JobQStart.sql 11806 2014-09-18 00:48:32Z jrms $

DROP PROCEDURE IF EXISTS JobQStart;

DELIMITER //
CREATE PROCEDURE JobQStart(
    IN job_id char(41),
    IN user_id int(10),
    IN siteenv_id int(10),
    IN cmd_name varchar(64),
    IN cmd_args varchar(512),
    IN tstamp_start int(10),
    IN adm_log binary(1))
BEGIN
    INSERT INTO `jobq`
        VALUES (
            job_id,
            user_id,
            siteenv_id,
            cmd_name,
            cmd_args,
            9999,
            '',
            tstamp_start,
            0,
            'START',
            adm_log
        )
    ;
    COMMIT;
END //
DELIMITER ;
