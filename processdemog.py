import re
import csv
user_file = open('/tmp/demog.csv', 'r')
user_file.readline()

write_file = open('/tmp/demog_proc.csv', 'w')

user_file_csv = csv.reader(user_file, delimiter=',', escapechar='/')
writer = csv.writer(write_file, dialect='excel')


data = []

print "dumping data"

for row in user_file_csv:
	row[3] = re.sub(r'\"', '', row[3])
	row[4] = re.sub(r'\"', '', row[4])
	row[5] = re.sub(r'\"', '', row[5])
	row[6] = re.sub(r'\"', '', row[6])
	row[7] = re.sub(r'\"', '', row[7])
	row[8] = re.sub(r'\"', '', row[8])
	row[9] = re.sub(r'\"', '', row[9])
	row[10] = re.sub(r'\"', '', row[10])
	row[11] = re.sub(r'\"', '', row[11])
	row[13] = re.sub(r'\"', '', row[13])
	row[14] = re.sub(r'\"', '', row[14])
	data.append(row)

print "writing data"
writer.writerows(data)

write_file.close()
