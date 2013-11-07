from pymongo import database,MongoClient
import json
from mbid.settings import BOT_NAME

connection = MongoClient()
db = database.Database(connection, BOT_NAME )

class MongoPipeline(object):
    def process_item(self, item, spider):
    	setattr(self, 'spider', spider)
    	db[self.spider.name].insert(dict(item))
        return item