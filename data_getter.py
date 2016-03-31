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

for month in calendar:
	for d in xrange(1, month[1] + 1):
		d_name = month[0] + '_' + str(d)
		day = wikipedia.page(d_name).content
		c = 0
		for index in xrange(0, len(categories) - 1):
			category = (day[day.find(categories[index][1]) + len(categories[index][1]):
						day.find(categories[index + 1][1])].split('\n'))

			for text_line in category:
				if text_line:
					line = re.split(u"\u2013", text_line)
					if len(line) < 2:
						year = '0'
		  				text = line[0]
					else:
						year = line[0][:-1]
						text = line[1]
					res = db.wiki.insert({
						'year': year,
						'info': text,
						'day': d_name,
						'category': categories[index][0]
						})
					c += 1
		print("day: " + d_name + " has " + str(c) + " entries\n")