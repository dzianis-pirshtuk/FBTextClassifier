#!/usr/bin/python
import psycopg2
import happyfuntokenizing
import re
from guess_language import guess_language
from collections import Counter

#Setup global objects
conn = psycopg2.connect(database="MyPersonality", user="postgres",password="qwerty", host="localhost")
tokenizer = happyfuntokenizing.Tokenizer(preserve_case = True)
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
	
def is_all_caps(word):

	num_upper = len(re.findall(r'[A-Z]',word))
	num_lower = len(re.findall(r'[a-z]',word))

	return (num_lower == 0 & float(num_upper)/len(word) > 0.55 )



print "userid: " + userid
while status != None:
	# For each status update, add to TF counter

	if guess_language.guessLanguage(status[2]) == "en":

		print type(status[2])
		#Counting the number of times lengthening occurs, and then normalizing it before token count.
		num_lengthens = len(re.findall(r'(.)\1{2,}',status[2]))
		status_term_count["aaaa_lengthen_count"] += num_lengthens
		text = re.sub(r'(.)\1{2,}',r'\1\1\1',status[2])

		terms = tokenizer.tokenize(text)
		for token in terms:

			if happyfuntokenizing.emoticon_re.search(token) != None:

				#Checking to see if token is in all caps.
				if is_all_caps(token):
					status_term_count["aaaa_caps_count"] += 1

				token = token.lower()

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
