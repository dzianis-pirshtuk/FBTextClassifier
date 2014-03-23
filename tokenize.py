import psycopg2
import happyfuntokenizing

conn = psycopg2.connect(database="MyPersonality", user="postgres",password="qwerty", host="localhost")

status_cur = conn.cursor()
tf_cur = conn.cursor()

tf_cur.execute("DROP TABLE IF EXISTS user_tf")
tf_cur.execute("create table user_tf (userid char(32), term varchar, termcnt integer, primary key(userid, term));")

status_cur.execute("SELECT * FROM user_status")

status_update = ()

tokenizer = happyfuntokenizing.Tokenizer(preserve_case = False)

while status_update != None:

	status_update = status_cur.fetchone()

	terms = tokenizer.tokenize(status_update[2])

	print "status"

	for term in terms:

		update_cmd = "UPDATE user_tf SET termcnt=termcnt+1 WHERE userid='" + status_update[0] + "' AND term='" + term + "';"

		insert_cmd = "INSERT INTO user_tf (userid, term, termcnt) SELECT '" + status_update[0] + "', '" + term + "', 5 WHERE NOT EXISTS (SELECT 1 FROM user_tf WHERE userid='" + status_update[0] + "' AND term='" + term + "');"

       
		tf_cur.execute(update_cmd)
		tf_cur.execute(insert_cmd)
