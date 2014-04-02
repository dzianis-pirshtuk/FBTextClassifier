#!/usr/bin/python

import psycopg2
import math

class ClassicRocchio:
    # Database constants
    primaryKey = "userid"
    tfTable = "user_status_tf"
    userInfoTable = "user_info"
    
    # SQL query templates
    findPossibleValues = """
    SELECT DISTINCT {attributeName}
    FROM {userInfoTable}
    WHERE {attributeName} NOT NULL
    """
    
    findDatasetSize = """
    SELECT COUNT({primaryKey})
    FROM {userInfoTable}
    WHERE {attributeName} NOT NULL
    """
    
    createView = """
    CREATE VIEW {viewName} AS
        SELECT * FROM {tfTable}
        WHERE {primaryKey} IN (
            SELECT {primaryKey} FROM {userInfoTable}
            WHERE {attributeName} NOT NULL
            OFFSET {offset}
            LIMIT {limit}
        ) 
    """
    
    dropView = """
    DROP VIEW {viewName}
    """
    
    idfQuery = """
    
    """
    
    def __init__(self, attributeName, conn):
        self.dbConn = conn;
        
        # Find the number of users with this attribute
        userCount = self.dbConn.cursor()
        q = ClassicRocchio.findDatasetSize.format(
            primaryKey=ClassicRocchio.primaryKey,
            userInfoTable=ClassicRocchio.userInfoTable,
            attributeName=attributeName
            )
        userCount.execute(q)
        
        //self.numUsers = userCount[0][0]
        
        
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

select 
