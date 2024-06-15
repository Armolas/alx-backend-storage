-- ComputeAverageWeightedScoreForUsers.sql

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE user_id INT;

    -- Cursor for iterating over user ids
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;

    -- Handler for cursor end
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- Open cursor
    OPEN user_cursor;

    -- Iterate over each user id
    read_loop: LOOP
        FETCH user_cursor INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Compute and update the average weighted score for the current user
        CALL ComputeAverageWeightedScoreForUser(user_id);
    END LOOP;

    -- Close cursor
    CLOSE user_cursor;
END //

DELIMITER ;
