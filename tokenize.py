#!/usr/bin/python
import psycopg2
import happyfuntokenizing
from collections import Counter

#Setup global objects
conn = psycopg2.connect(database="MyPersonality", user="postgres",password="qwerty", host="localhost")
tokenizer = happyfuntokenizing.Tokenizer(preserve_case = False)
insert_cmd = "INSERT INTO user_tf (userid, term, termcnt) VALUES(%s, %s, %s)"

# user status selector curr
status_cur = conn.cursor("status_cur")
status_cur.execute("SELECT * FROM user_status ORDER BY userid;")

# Destroy-Create target table
tf_cur = conn.cursor()
tf_cur.execute("DROP TABLE IF EXISTS user_tf")
tf_cur.execute("create table user_tf (userid char(32), term varchar, termcnt integer, primary key(userid, term));")

# Get all of the status updates for each userid in a loop
status = status_cur.fetchone()
userid = status[0]
status_term_count = Counter()
	
		

print "userid: " + userid
while status != None:
	# For each status update, add to TF counter
	terms = tokenizer.tokenize(status[2])
	for token in terms:
		status_term_count[token] += 1
		#print token
	status = status_cur.fetchone()
	if status == None or userid != status[0]:
		tup = []
		for token, cnt in status_term_count.items():
			if token != None:
				tup.append((userid, token, cnt))
		if(len(tup) > 0):
			args_str = ",".join(cur.mogrify("(%s, %s, %s)", x) for x in tup)
			tf_cur.execute("INSERT INTO user_tf (userid, term, termcnt) VALUES " + args_str)
		status_term_count = Counter()
		if status != None:		
			userid = status[0]
			print "userid: " + userid

#commit changes back to DB
conn.commit()
