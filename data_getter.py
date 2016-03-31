import wikipedia
import re
from pymongo import MongoClient

calendar = [('January', 31), ('February', 29), 
			 ('March', 31), ('April', 30), 
			 ('May', 31), ('June', 30),
			 ('July', 31), ('August', 31),
			 ('September', 30), ('October', 31),
			 ('November', 30), ('December', 31)]

categories = [('events', '== Events =='),
			  ('births', '== Births =='), 
			  ('deaths', '== Deaths =='), 
			  ('observances', '== Holidays and observances =='),
			  ('dummy', '== External links ==')]

client = MongoClient()
db = client.homework

def insert_to_db(line):
	if len(line) < 2: year, text = '0', line[0] #observances have no year
	else: year, text = line[0][:-1], line[1] #-1 slicing to remove \n

	res = db.wiki.insert({
		'year': year,
		'info': text,
		'day': day_name,
		'category': categories[categ_index][0]
		})
	return res

for month in calendar:
	for day_index in xrange(1, month[1] + 1):
		day_name = month[0] + '_' + str(day_index)
		day_content = wikipedia.page(day_name).content
		count = 0

		for categ_index in xrange(0, len(categories) - 1):
			left_index = (day_content.find(categories[categ_index][1]) + 
						  len(categories[categ_index][1]))
			right_index = day_content.find(categories[categ_index + 1][1])
			category_content = (day_content[left_index : right_index].split('\n'))
			#get only the content between '== this1 ==' and '== this2 =='

			for line in category_content:
				if line:
					line = re.split(u"\u2013", line) #remove the dashes
					insert_to_db(line)
					count += 1
		print("Inserted " + str(count) + " entries for " + day_name)