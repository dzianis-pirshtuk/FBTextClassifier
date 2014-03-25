#!/usr/bin/python
import psycopg2
import happyfuntokenizing
from collections import Counter

conn = psycopg2.connect(database="MyPersonality", user="postgres",password="qwerty", host="localhost")
# Set encoding to target DB encoding
conn.set_client_encoding('WIN1252')

# Make a server-side cursor (should fetch 2k at a time)
status_cur = conn.cursor(name='status_cur')
tf_cur = conn.cursor()

tf_cur.execute("DROP TABLE IF EXISTS user_tf")
tf_cur.execute("create table user_tf (userid char(32), term varchar, termcnt integer, primary key(userid, term));")

status_cur.itersize = 2000
status_cur.execute("SELECT * FROM user_status")

status_update = status_cur.fetchone()

tokenizer = happyfuntokenizing.Tokenizer(preserve_case = False)


while status_update != None:

	print "status: " + str(status_cur.rownumber) + "/" + str(status_cur.rowcount) + " " + str(status_update)
	
	status_term_count = Counter()

	terms = tokenizer.tokenize(status_update[2])	

	for token in terms:
		status_term_count[token] += 1

	for token, cnt in status_term_count.items():

		update_cmd = "UPDATE user_tf SET termcnt=termcnt+%s WHERE userid=%s AND term=%s;"

		insert_cmd = "INSERT INTO user_tf (userid, term, termcnt) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM user_tf WHERE userid=%s AND term=%s);"

       		print token
		tf_cur.execute(update_cmd, (cnt, status_update[0], token))
		tf_cur.execute(insert_cmd, (status_update[0], token, cnt, status_update[0], token))
	
	status_update = status_cur.fetchone()

#commit changes back to DB for all status updates and begin new XACT
conn.commit()
