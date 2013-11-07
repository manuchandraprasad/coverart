from pymongo import MongoClient
#connection = MongoClient('db.image-quick.com')
#connection = MongoClient('10.0.0.10:27017')
#db_ip = 'localhost'
db_ip = 'localhost'
connection = MongoClient(db_ip)
db = connection.imagequick_dev

