#!/usr/bin/python

import psycopg2
import math

tfs = "SELECT userid, term, cnt FROM user_status_tf ORDER BY userid"
userInfo = "SELECT userid, gender FROM user_demog WHERE (ud.locale='en_US' OR ud.locale='en_GB') AND ud.userid IN (SELECT userid from user_status);"
idfs = """SELECT term, LN((SELECT COUNT(*) FROM trainingInfo)::float / COUNT(userid)) AS idf
        FROM trainingData
        GROUP BY term;"""

conn = psycopg2.connect(database="MyPersonality", user="postgres",password="qwerty", host="localhost")

tfCursor = conn.cursor("x")
tfCursor.execute(tfs);

userInfoCursor = conn.cursor("y")
userInfoCursor.execute(userInfo)


num_correct = 0


user_list = []
tf_dict = {}
idf_dict = {}

info_dict = {}

rep_vectors_dict = {}

def ln_tf_idf(tf,idf):

	return (math.log(float(1 + tf),2) * math.log((float(len(user_list)) / idf),2))

def vect_length(vect):
	
	length = 0.0

	for key in vect:
		
		length += (tf_idf(vect[key],idf_dict[vect[key]]+1) ** 2)

	length = (length ** 0.5)

	return length 		

def construct_rep_vectors(i):

	userid = user_list[i]
	usertype = info_dict[userid]

	if usertype not in rep_vectors_dict:

		rep_vectors_dict[usertype] = dict()

	for term in tf_dict[userid]:

		w = ln_tf_idf(tf_dict[userid][term],idf_dict[term])

		if term in rep_vectors_dict[usertype]:
			rep_vectors_dict[usertype][term] += w
		else:
			rep_vectors_dict[usertype][term] = w



def norm_tf_idf_sscore(i, query_dict,doc_dict):

	score = 0.0

	for key in query_dict:

		if key in doc_dict:

			score += (tf_idf(query_dict[key],idf_dict[key])*tf_idf(doc_dict[key],idf_dict[key]))

	q_v_len = vect_length(query_dict)
	d_v_len = vect_length(doc_dict)

	score = (score / (q_v_len*d_v_len))

	return score

def construct_idf_dict():

	temp_tf_dict = {}
	user_id = ""

	for tfEntry in tfCursor:
	    
		if (user_id != tfEntry[0]):

			if (user_id != ""):

				user_list.append(userid)
				tf_dict[user_id] = temp_tf_dict
				temp_tf_dict.clear()

			user_id = tfEntry[0]

		temp_tf_dict[tfEntry[1]] = tfEntry[2]

		if tfEntry[1] in idf_dict:
			idf_dict[tfEntry[1]] += 1
		else:
			idf_dict[tfEntry[1]] = 1

def construct_info_dict():

	for userInfoEntry in userInfoCursor:

		info_dict[userInfoEntry[0]] = userInfoEntry[1]



def fold_iteration(lower_fold_ind, upper_fold_ind):

	num_correct = 0

	test_idf_dict = {}

	for i in range(lower_fold_ind,upper_fold_ind):

		for term in tf_dict[user_list[i]]:
			
			if term in test_idf_dict:
				test_idf_dict[term] += 1
			else:
				test_idf_dict[term] = 1


	for key_val in test_idf_dict.items():

		idf_dict[key_val[0]] -= key_val[1]

		if idf_dict[key_val[0]] == 0:
			idf_dict.remove(key_val[0])


	for i in range(0,lower_test_ind+1):

		construct_rep_vectors(i)

	for i in range(higher_test_ind, len(user_list)):

		construct_rep_vectors(i)



	for i in range(lower_fold_ind,higher_fold_ind):

		userid = user_list[i]

		max_sim_score = -1.0
		prediction = ""

		for rep_vector in rep_vectors_dict.items():

			sim_score = norm_tf_idf_sscore(idf_dict[userid], rep_vector[1])

			if sim_score > max_sim_score:

				max_sim_score = sim_score
				prediction = rep_vector[0]


		if prediction == info_dict[userid]:

			num_correct += 1


	for key_val in test_idf_dict.items():

		if key_val[0] in idf_dict:
			idf_dict[key_val[0]] += key_val[1]
		else 
			idf_dict[key_val[0]] = key_val[1]

	return num_correct





def main():

	construct_info_dict()
	construct_idf_dict()


	total_correct_predictions = 0

	num_folds = raw_input("How many folds?")

	sizeof_fold = len(user_list)/num_folds

	for i in range(num_folds)

		lower_fold_ind = i*sizeof_fold
		if i = num_folds -1
			higher_fold_ind = len(user_list)
		else
			higher_fold_ind = lower_fold_ind + sizeof_fold + 1

	total_correct_predictions += fold_iteration(lower_fold_ind,higher_fold_ind)

	print "Prediction accuracy", float(total_correct_predictions)/len(user_list)





    
if __name__ == '__main__':
    main()
