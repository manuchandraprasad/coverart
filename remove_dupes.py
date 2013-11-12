from config import db
import json
import requests
from pprint import pprint
from progressbar import ProgressBar,Bar,Percentage
from pymongo import MongoClient
#connection = MongoClient('db.image-quick.com')
#connection = MongoClient('10.0.0.10:27017')
#db_ip = 'localhost'
db_ip = 'localhost'
#db_ip = 'db.image-quick.com'
connection = MongoClient(db_ip)
db = connection.album_art
i=0
hooks = []
tot = db.itunes_store_found.find().count()
pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=tot).start()

for hook in db.itunes_store_found.find():
    del hook['_id']
    hooks.append(hook)
print "Total Dupes : %d"%(tot-len(list(set(hooks))))
for hook in list(set(hooks)): 
    db.found.insert(hook)
    i+=1
    pbar.update(i)
pbar.finish()
