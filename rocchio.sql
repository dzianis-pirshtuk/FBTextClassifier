CREATE TABLE user_demog_locale AS
		SELECT * FROM user_demog WHERE 
		userid IN (SELECT userid FROM user_status_tf)
		AND (locale='en_US' OR locale='en_GB');

CREATE OR REPLACE VIEW testInfo AS
        SELECT * FROM user_demog_locale
        WHERE gender IS NOT NULL 
        ORDER BY userid
        OFFSET 9000
        LIMIT 1000;
        
CREATE OR REPLACE VIEW testData AS
        SELECT * FROM user_status_tf
        WHERE userid IN (
            SELECT userid FROM testInfo
        );

CREATE OR REPLACE VIEW trainingInfo AS
        SELECT * FROM user_demog_locale
        WHERE gender IS NOT NULL 
        ORDER BY userid
        OFFSET 0
        LIMIT 9000;
        
CREATE OR REPLACE VIEW trainingData AS
        SELECT * FROM user_status_tf
        WHERE userid IN (
            SELECT userid FROM trainingInfo
        );
        
CREATE OR REPLACE VIEW termIDFs AS
        SELECT term, LN((SELECT COUNT(*) FROM trainingInfo)::float / COUNT(userid)) AS idf
        FROM trainingData
        GROUP BY term;
        
CREATE OR REPLACE VIEW termWeights AS
        SELECT Tr.gender, T.term, (SUM(LN(1 + T.cnt)) * I.idf) AS weight
        FROM trainingData T, trainingInfo Tr, termIDFs I
        WHERE Tr.userid = T.userid AND I.term = T.term
        GROUP BY Tr.gender, T.term, I.idf;
        
CREATE OR REPLACE VIEW prototypeVectorLengths AS
        SELECT gender, SQRT(SUM(weight * weight)) AS vectorLength
        FROM termWeights
        GROUP BY gender;
        
CREATE OR REPLACE VIEW userWeights AS
        SELECT T.userid, T.term, LN(1 + T.cnt) * I.idf AS weight
        FROM testData T, termIDfs I
        WHERE T.term = I.term;
        
CREATE OR REPLACE VIEW userVectorLengths AS
        SELECT userid, SQRT(SUM(weight * weight)) AS vectorLength
        FROM userWeights
        GROUP BY userid;
        
CREATE OR REPLACE VIEW results AS
        SELECT U.userid, W.gender, 
            (SUM(U.weight * W.weight) / (UVLen.vectorLength * PVLen.vectorLength)) AS cosSim
        FROM userWeights U, termWeights W, userVectorLengths UVLen, prototypeVectorLengths PVLen
        WHERE U.userid = UVLen.userid AND U.term = W.term AND W.gender = PVLen.gender
        GROUP BY U.userid, UVLen.vectorLength, W.gender, PVLen.vectorLength;
        
SELECT COUNT(R1.userid) FROM results R1, testInfo D
    WHERE (R1.userid, R1.cosSim) IN (
        SELECT R2.userid, MAX(R2.cosSim) FROM results R2 GROUP BY R2.userid 
    ) AND d.gender=r1.gender AND d.userid=r1.userid;