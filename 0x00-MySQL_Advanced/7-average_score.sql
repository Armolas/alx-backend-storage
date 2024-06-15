-- ComputeAverageScoreForUser.sql

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE project_count INT;
    DECLARE avg_score FLOAT;

    -- Calculate the total score and the number of projects for the user
    SELECT 
        SUM(score) INTO total_score, 
        COUNT(*) INTO project_count
    FROM 
        corrections
    WHERE 
        user_id = user_id;

    -- Calculate the average score
    IF project_count > 0 THEN
        SET avg_score = total_score / project_count;
    ELSE
        SET avg_score = 0;
    END IF;

    -- Update the users table with the average score
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END //

DELIMITER ;
