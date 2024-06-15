-- ComputeAverageWeightedScoreForUsers.sql

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE user_id INT;
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight INT;
    DECLARE avg_weighted_score FLOAT;
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN user_cursor;

    read_loop: LOOP
        FETCH user_cursor INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Reset variables
        SET total_weighted_score = 0;
        SET total_weight = 0;
        SET avg_weighted_score = 0;

        -- Calculate the total weighted score and total weight for the current user
        SELECT 
            SUM(c.score * p.weight) AS total_weighted_score, 
            SUM(p.weight) AS total_weight
        INTO 
            total_weighted_score, 
            total_weight
        FROM 
            corrections c
        JOIN 
            projects p ON c.project_id = p.id
        WHERE 
            c.user_id = user_id;

        -- Calculate the average weighted score
        IF total_weight > 0 THEN
            SET avg_weighted_score = total_weighted_score / total_weight;
        ELSE
            SET avg_weighted_score = 0;
        END IF;

        -- Update the users table with the average weighted score
        UPDATE users
        SET average_score = avg_weighted_score
        WHERE id = user_id;
    END LOOP;

    CLOSE user_cursor;
END //

DELIMITER ;
