#!/usr/bin/python

import psycopg2
import math

tfs = "SELECT userid, term, LN(1 + cnt) FROM user_status_tf ORDER BY userid"
userInfo = "SELECT userid, gender FROM user_demog WHERE (ud.locale='en_US' OR ud.locale='en_GB') AND ud.userid IN (SELECT userid from user_status);"
idfs = """SELECT term, LN((SELECT COUNT(*) FROM trainingInfo)::float / COUNT(userid)) AS idf
        FROM trainingData
        GROUP BY term;"""

conn = psycopg2.connect(database="MyPersonality", user="postgres",password="qwerty", host="localhost")

tfCursor = conn.cursor()
tfCursor.execute(tfs);



for tfEntry in tfCursor:
    print tfEntry[0]
    print tfEntry[1]
    
