from flask import Flask
from flask import request
from bson.json_util import dumps
from pymongo import MongoClient

client = MongoClient()
db = client.homework

app = Flask(__name__)

def get_query(year = None, day = None, category = None):
	if (not year and not day and not category): return "Hello ^_^"
	loc = locals()
	criteria = {k:loc[k] for k in loc if loc[k] != None}
	return db.wiki.find(criteria, {'_id': False})

@app.route('/', methods = ['GET'])
def get_req():
	year = request.args.get('year')
	day = request.args.get('day')
	category = request.args.get('category')

	exp = get_query(year, day, category)
	return dumps({'results': list(exp)},
		ensure_ascii = False,
		indent = 4).encode('utf8')

if __name__ == '__main__':
	app.run()