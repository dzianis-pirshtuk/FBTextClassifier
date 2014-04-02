#!/usr/bin/python
import psycopg2
import happyfuntokenizing
import re
import csv
import codecs
from collections import Counter

#Setup global objects
conn = psycopg2.connect(database="MyPersonality", user="postgres",password="qwerty", host="localhost")
tokenizer = happyfuntokenizing.Tokenizer(preserve_case = True)
tf_file = open('/tmp/user_status_tf.csv', 'w')
len_file = open('/tmp/user_status_len.csv', 'w')
caps_file = open('/tmp/user_status_caps.csv', 'w')
tf_csv = csv.writer(tf_file, dialect='excel')
len_csv = csv.writer(len_file, dialect='excel')
caps_csv = csv.writer(caps_file, dialect='excel')

# user status selector curr
status_cur = conn.cursor("status_cur")
status_cur.itersize = 1000000 #I'm hoping you can load this much into memory... (you probably can)
status_cur.execute("SELECT * FROM user_status ORDER BY userid;")

# Get all of the status updates for each userid in a loop
def is_all_caps(word):
	num_upper = len(re.findall(r'[A-Z]',word))
	num_lower = len(re.findall(r'[a-z]',word))
	return ((num_lower == 0) & (float(num_upper)/len(word) > 0.55 ) & (len(word) > 1))

if __name__ == '__main__':
	userid = None
	lengthencount = 0
	capscount = 0
	status_term_count = Counter()
	status = None
	for row in status_cur:
		# If this is a new userid, then flush the buffer to the files
		if userid != row[0]:
			tup = []
			for token, cnt in status_term_count.items():
				if token != None and token != "":
					tup.append((userid, token.encode('utf-8'), cnt))
			if(len(tup) > 0):
				tf_csv.writerows(tup)
				len_csv.writerow((userid, lengthencount))
				caps_csv.writerow((userid, capscount))
			status_term_count = Counter()
			userid = row[0]
			print "userid: " + userid
			lengthencount = 0
			capscount = 0
			
		#I add a trailing whitespace to make my regexes work correctly, this is important.
		status_update = row[2] + ' '
		#Counting the number of times lengthening occurs. Not treating ellipse as instance of lenghtening, though lengthened ellipses (e.g '.....') are counted.
		lengthencount += (len(re.findall(r'(.)\1{2,}',status_update)) - len(re.findall(r'[^\.][\.]{3}[^\.]',status_update)))
		#...and then normalizing all lengthengings to 3 repetitions (e.g. Yesssss becomes Yesss)
		status_update = re.sub(r'(.)\1{2,}',r'\1\1\1',status_update)

		terms = tokenizer.tokenize(status_update)
		for token in terms:
			#Caps checking does not apply to emoticons.
			if happyfuntokenizing.emoticon_re.search(token) == None:
				#Checking to see if token is in all caps.
				if is_all_caps(token):
					capscount += 1
				#lower_casing all words which are not emoticons. Emoticons cant have case changed (e.g. =D != =d)
				token = token.lower()

			status_term_count[token] += 1
			#print token

	#Flush whatever might be left from the last parse
	tup = []
	for token, cnt in status_term_count.items():
		if token != None and token != "":
			tup.append((userid, token, cnt))
	if(len(tup) > 0):
		tf_csv.writerows(tup)
	status_term_count = Counter()
	userid = row[0]
	print "userid: " + userid
	lengthencount = 0
	capscount = 0
	#commit changes back to DB
	conn.commit()
