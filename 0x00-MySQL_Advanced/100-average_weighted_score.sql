-- Add column to store average weighted score
ALTER TABLE users ADD COLUMN average_weighted_score FLOAT DEFAULT 0;

-- ComputeAverageWeightedScoreForUser.sql

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score FLOAT DEFAULT 0;
    DECLARE total_weight FLOAT DEFAULT 0;
    DECLARE avg_weighted_score FLOAT;

    -- Calculate the total weighted score and total weight
    SELECT SUM(score * project_id), SUM(project_id)
    INTO total_weighted_score, total_weight
    FROM corrections
    WHERE user_id = user_id;

    -- Calculate the average weighted score
    IF total_weight > 0 THEN
        SET avg_weighted_score = total_weighted_score / total_weight;
    ELSE
        SET avg_weighted_score = 0;
    END IF;

    -- Update the users table with the average weighted score
    UPDATE users
    SET average_weighted_score = avg_weighted_score
    WHERE id = user_id;
END //

DELIMITER ;
