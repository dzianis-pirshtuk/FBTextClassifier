#!/usr/bin/python

import psycopg2
import math



def getPrototypeVectors(attributeName, conn):
    # create view TestUserData as select 

    # Get the possible values for this attribute
    q1 = 'SELECT DISTINCT(%s) WHERE %s NOT NULL'
    uniq_cur = conn.cursor()
    uniq_cur.execute(q1, (attributeName, ))

    categories = [r[0] for r in uniq_cur]
    
    doc
    
    
    # For each possible category, find the prototype vector
    for c in categories:
        query = 'select'
    


def main():
    conn = psycopg2.connect(database="MyPersonality", user="postgres",password="qwerty", host="localhost")

select 
