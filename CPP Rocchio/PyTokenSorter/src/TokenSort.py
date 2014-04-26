from _collections import defaultdict
import csv
from operator import itemgetter
import re

import happyfuntokenizing
from nltk.stem.porter import PorterStemmer

#Some interesting ones:
# 1: gender
# 3: age
# 4: relationship_status
target = 1
stem = False
stopwordRemoval = False

def fileToSet(f):
    toReturn = set()
    while 1:
        ln = f.readline()
        if ln == '':
            return toReturn
        toReturn.add(ln.rstrip())

if __name__ == "__main__":
    stemmer = PorterStemmer()
    stopwordsfile = open("../stopwords")
    stopWords = fileToSet(stopwordsfile)

    #Open files of interest
    user_status_file_in = open('../user_status.csv')
    demog_file_in = open('../demog.csv')

    #Remove the first line of each file (it's just a header)
    user_status_file_in.readline()
    demog_file_in.readline()

    #Construct their representations in memory, as relates to their userid field
    user_status_dict = defaultdict(list)
    demog_dict = defaultdict(tuple)

    print "[X] Parsing initial data"

    #(1/2) demog_file
    print "    [+] DEMOG.CSV"
    demog_csv_in = csv.reader(demog_file_in, delimiter=",", escapechar='/')
    print "        [*] Dumping data into RAM"
    for row in demog_csv_in:
        if row[target] != "" and (row[12] == 'en_US' or row[12] == 'en_GB'):
            demog_dict[row[0]] = row[target]
#             if int(row[target]) < 19:
#                 demog_dict[row[0]] = (0,)
#             else:
#                 if int(row[target]) < 23:
#                     demog_dict[row[0]] = (1,)
#                 else:
#                     if int(row[target]) < 30:
#                         demog_dict[row[0]] = (2,)
#                     else:
#                         demog_dict[row[0]] = (3,)


    #(2/2) user_status_file
    print "    [+] USER_STATUS.CSV"
    user_status_csv_in = csv.reader(user_status_file_in, delimiter=",", escapechar='/')
    print "        [*] Dumping data into RAM (with intersection)"
    for row in user_status_csv_in:
        if row[0] in demog_dict:
            user_status_dict[row[0]].append(row[2])
    print "        [*] Removing entries in DEMOG that are not in USER_STATUS"
    user_status_demog_removal = demog_dict.viewkeys() - user_status_dict.viewkeys()
    for key in user_status_demog_removal:
        del demog_dict[key]

    #Some pretty print output to make you feel good
    print "    [+] PARSED USERS: " + str(len(demog_dict.viewkeys()))
    print "    [+] PARSED STATUS UPDATES: " + str(len(user_status_dict.viewkeys()))

    #Write everything we can to free up memory
    print "[X] Writing DEMOG_PROC.CSV"
    demog_file_out = open('../demog_proc.csv', 'w')
    demog_csv_out = csv.writer(demog_file_out, dialect='excel')
    demog_csv_out.writerows((k,) + tuple(v) for k, v in demog_dict.iteritems())
    demog_file_out.close()

    del demog_dict

    #Start tokenizing status updates (and delete them from the map as we go to save memory 0.o)
    print "[X] Tokenizing (and writing) USER_STATUS"
    userids = set(user_status_dict.viewkeys())
    tokenizer = happyfuntokenizing.Tokenizer(preserve_case=False)

    user_status_tf_file_out = open('../user_status_tf_proc.csv', 'w')
    user_status_tf_csv_out = csv.writer(user_status_tf_file_out, dialect='excel')

    for userid in userids:
        lengcount = 0
        temp_tokens = defaultdict(int)
        for update in user_status_dict[userid]:
            terms = tokenizer.tokenize(re.sub(r'\n', ' ', update))
            for term in terms:
                if stopwordRemoval and term in stopWords:
                    continue
                if stem:
                    temp_tokens[stemmer.stem(term)] += 1
                else:
                    temp_tokens[term] += 1
                #lengcount += (len(re.findall(r'(.)\1{2,}',term)) - len(re.findall(r'[^\.][\.]{3}[^\.]',term)))
        del user_status_dict[userid]
        user_status_tf_csv_out.writerows((userid, cnt, term.encode("UTF-8")) for term, cnt in temp_tokens.iteritems())
        #user_status_tf_csv_out.writerow((userid, lengcount, "xxxx_leng"))
        #xxxx_leng
        if len(user_status_dict) % 1000 == 0:
            #print("\r    [*] to go: {0}".format(len(user_status_dict))),
            print("    [*] to go: {0}".format(len(user_status_dict)))

    print
    print "[X] DONE!!! :D"

    user_status_tf_file_out.close()
