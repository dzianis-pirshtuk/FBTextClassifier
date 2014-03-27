#!/usr/bin/python
import psycopg2
import happyfuntokenizing
from collections import Counter

#Setup global objects
conn = psycopg2.connect(database="MyPersonality", user="postgres",password="qwerty", host="localhost")
tokenizer = happyfuntokenizing.Tokenizer(preserve_case = False)
insert_cmd = "INSERT INTO user_tf (userid, term, termcnt) VALUES(%s, %s, %s)"
select_cmd = "SELECT * FROM user_status WHERE userid=%s"

# user status selector curr
status_cur = conn.cursor()

# Destroy-Create target table
tf_cur = conn.cursor()
tf_cur.execute("DROP TABLE IF EXISTS user_tf")
tf_cur.execute("create table user_tf (userid char(32), term varchar, termcnt integer, primary key(userid, term));")

# Make a server-side cursor to get list of userids (should fetch 2k at a time)
userid_cur = conn.cursor(name='userid_cur')

userid_cur.itersize = 2000
userid_cur.execute("SELECT DISTINCT userid FROM user_status")
userid = userid_cur.fetchone()[0]

# Get all of the status updates for each userid in a loop
while userid != None:
	print "userid: " + userid
	status_term_count = Counter()
	status_cur.execute(select_cmd, (userid, ))
	status_update = status_cur.fetchone()
	# For each status update, add to TF counter
	while status_update != None:
		terms = tokenizer.tokenize(status_update[2])
		for token in terms:
			status_term_count[token] += 1
	       		#print token
		status_update = status_cur.fetchone()
	for token, cnt in status_term_count.items():
		tf_cur.execute(insert_cmd, (userid, token, cnt))
	userid = userid_cur.fetchone()[0]

#commit changes back to DB
conn.commit()
