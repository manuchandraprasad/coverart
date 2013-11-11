from config import db
import json
import requests
from pprint import pprint
from progressbar import ProgressBar,Bar,Percentage
from pymongo import MongoClient
#connection = MongoClient('db.image-quick.com')
#connection = MongoClient('10.0.0.10:27017')
db_ip = 'localhost'
#db_ip = 'localhost'
#db_ip = 'db.image-quick.com'
connection = MongoClient(db_ip)
db = connection.album_art

import csv
targets = []
try:
    f = open('artist_titles_albums.csv','rt')
    fieldnames = ('artist', 'title', 'album')
    reader = csv.DictReader(f, fieldnames=fieldnames)
    for hook in reader:
        targets.append(hook)
finally:
    f.close()

pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(targets)).start()
i=0

for hook in targets:
    try:
        link = 'https://itunes.apple.com/search?term=%s' % (
            hook['artist'] + '+' + hook['album']).replace(' ', '+')
        print "[FETCH] %s - %s "%(hook['artist'],hook['album'])
        apple_api = requests.get(link)
        results = json.loads(apple_api.content)['results']
        if results:
            print "[FOUND] %s - %s "%(hook['artist'],hook['album'])
            hook['album_art'] = results[0]['artworkUrl100']
            hook['data'] = results[0]
            db.itunes_store_found.insert(hook)
        else:
            print "[FAIL] %s - %s "%(hook['artist'],hook['album'])
            db.itunes_store_not_found.insert(hook)
    except:
        print "[FAIL][HTTP] %s - %s "%(hook['artist'],hook['album'])
        db.itunes_store_not_found.insert(hook)
    i+=1;
    pbar.update(i)
pbar.finish()