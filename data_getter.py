import wikipedia
import datetime
import re
from pymongo import MongoClient
from pymongo import IndexModel, ASCENDING, DESCENDING

client = MongoClient()
db = client.homework
db.wiki.create_index([
			('category', ASCENDING),
			('year', ASCENDING),
			('day', ASCENDING),
			('title', ASCENDING)
			])
wikipedia.set_rate_limiting(True, min_wait=datetime.timedelta(0, 0, 20000))
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

def insert_to_db(line, day_n, categ_i):
	if len(line) < 2: year, text = '0', line[0] #observances have no year
	else: year, text = line[0][:-1], line[1] #-1 slicing to remove \n

	title = text[2:5]

	res = db.wiki.update_one(
		{
			'category': categories[categ_i][0],
			'year': year,
			'day': day_n,
			'title': title,
			'info': text
		},
		{
			'$set': {
				'category': categories[categ_i][0],
				'year': year,
				'day': day_n,
				'title': title,
				'info': text
			}
		},
		upsert=True
	)

	return res

def get_categ_content(content, c_index):
	l_index = (content.find(categories[c_index][1]) + 
						  len(categories[c_index][1]))
	r_index = right_index = content.find(categories[c_index + 1][1])
	return content[l_index : r_index]

def split_line(line):
	line = re.split(u"\u2013", line) #remove the dashes
	return line

def get_wiki_content(date): #for timing purpose, observation: very slow TODO: change scrapper
	return wikipedia.page(date).content

def update_db(db):
	
	for month in calendar:
		for day_index in xrange(1, month[1] + 1):
			count_up, count_ins = 0, 0
			day_name = month[0] + '_' + str(day_index)
			day_content = get_wiki_content(day_name)

			for categ_index in xrange(0, len(categories) - 1):
				category_content = get_categ_content(day_content, categ_index).split('\n')
				#get only the content between '== this1 ==' and '== this2 =='

				for line in category_content:
					if line:
						line = split_line(line)
						result = insert_to_db(line, day_name, categ_index)
						if result.modified_count != 0: count_up += 1
						elif result.matched_count == 0: count_ins += 1
			#print("Inserted " + str(count_ins) + ", Updated " + str(count_up) + " entries for " + day_name)
	print("Database update finished")

def main():

	print("Database update started")
	update_db(db)

main()