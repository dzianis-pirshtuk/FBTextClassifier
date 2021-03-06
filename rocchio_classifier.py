#!/usr/bin/python

import psycopg2
import math

class ClassicRocchio:
    # Database constants
    
    # SQL query templates
    findPossibleValues = """
    SELECT DISTINCT {attributeName}
    FROM user_demog
    WHERE {attributeName} NOT NULL
    """
    
    findDatasetSize = """
    SELECT COUNT(userid)
    FROM user_demog
    WHERE {attributeName} NOT NULL
    """
    
    createTestViews = """
    CREATE VIEW testInfo AS
        SELECT * FROM user_demog_good
        WHERE {attributeName} IS NOT NULL 
            AND (locale = 'en_US' OR locale = 'en_GB')
            AND userid IN (SELECT userid FROM user_status_tf)
        ORDER BY userid
        OFFSET {offset}
        LIMIT {limit}
    
    CREATE VIEW testData AS
        SELECT * FROM user_status_tf
        WHERE userid IN (
            SELECT userid FROM testInfo
        );
    """
    createTrainingViews = """
        
    CREATE VIEW trainingInfo AS
        SELECT * FROM user_demog
        WHERE {attributeName} IS NOT NULL 
            AND (locale = 'en_US' OR locale = 'en_GB')
            AND userid IN (SELECT userid FROM user_status_tf)
        ORDER BY userid
        OFFSET {offset}
        LIMIT {limit}
    
    CREATE VIEW trainingData AS
        SELECT * FROM user_status_tf
        WHERE userid IN (
            SELECT userid FROM trainingInfo
        );
    """
    
    
    dropView = """
    DROP VIEW {viewName}
    """
    
    idfQuery = """
    CREATE VIEW termIDFs AS
        SELECT term, LN((SELECT COUNT(*) FROM trainingInfo)::float / COUNT(userid)) AS idf
        FROM trainingData
        GROUP BY term
    """
    
    termWeightQuery = """
    CREATE VIEW termWeights AS
        SELECT Tr.{attributeName}, T.term, (SUM(LN(1 + T.cnt)) * I.idf) AS weight
        FROM trainingData T, trainingInfo Tr, termIDFs I
        WHERE Tr.userid = T.userid AND I.term = T.term
        GROUP BY Tr.{attributeName}, T.term, I.idf
    """
    
    prototypeVectorLengthsQuery = """
    CREATE VIEW prototypeVectorLengths AS
        SELECT {attributeName}, SQRT(SUM(weight * weight)) AS vectorLength
        FROM termWeights
        GROUP BY {attributeName}
    """
    
    userWeightsQuery = """
    CREATE VIEW userWeights AS
        SELECT T.userid, T.term, LN(1 + T.cnt) * I.idf AS weight
        FROM testData T, termIDfs I
        WHERE T.term = I.term
    """
    
    userVectorLengthsQuery = """
    CREATE VIEW userVectorLengths AS
        SELECT userid, SQRT(SUM(weight * weight)) AS vectorLength
        FROM userWeights
        GROUP BY userid
    """
    
    resultsViewQuery = """
    CREATE VIEW results AS
        SELECT U.userid, W.{attributeName}, 
            (SUM(U.weight * W.weight) / (UVLen.vectorLength * PVLen.vectorLength)) AS cosSim
        FROM userWeights U, termWeights W, userVectorLengths UVLen, prototypeVectorLengths PVLen
        WHERE U.userid = UVLen.userid AND U.term = W.term AND W.{attributeName} = PVLen.{attributeName}
        GROUP BY U.userid, UVLen.vectorLength, W.{attributeName}, PVLen.vectorLength
    """
    
    finalResultsQuery = """
    SELECT * FROM results R1
    WHERE R1.cossim = (
        SELECT MAX(R2.cossim)
        FROM results R2
        WHERE R2.userid = R1.userid
        )
    """
    
    

    def __init__(self, attributeName, numFolds, conn):
        self.dbConn = conn;
        
        # Find the number of users with this attribute
        userCount = self.dbConn.cursor()
        q = ClassicRocchio.findDatasetSize.format(
            primaryKey=ClassicRocchio.primaryKey,
            userInfoTable=ClassicRocchio.userInfoTable,
            attributeName=attributeName
            )
        userCount.execute(q)
        
        
        # self.numUsers = userCount[0][0]
        
        
        # Get the possible values for each attribute
        attrValues = self.dbConn.cursor()
        q = ClassicRocchio.findPossibleValues.format(
            attributeName=attributeName, 
            userInfoTable=ClassicRocchio.userInfoTable,
            )
        attrValues.execute(q)
    
        self.attributeValues = [r[0] for r in attrValues].sort()
        


def main():
    conn = psycopg2.connect(database="MyPersonality", user="postgres",password="qwerty", host="localhost")
