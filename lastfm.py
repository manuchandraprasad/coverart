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
import unicodedata
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
    hook['artist'] = unicode(hook['artist'], errors='ignore')
    hook['album'] = unicode(hook['album'], errors='ignore')
    hook['title'] = unicode(hook['title'], errors='ignore')  
    try:
        link = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=c85e43eeb52ffc10176d342353882057&artist=%s&album=%s&format=json' % (
            hook['artist'],hook['album'])
        print "[FETCH] %s - %s "%(hook['artist'],hook['album'])
        last_fm_api = requests.get(link)
        results = json.loads(apple_api.content)['results']
        if results:
            print "[FOUND] %s - %s "%(hook['artist'],hook['album'])
            db.lastfm_found.insert(results['album'])
        else:
            print "[FAIL] %s - %s "%(hook['artist'],hook['album'])
            db.lastfm_not_found.insert(hook)
    except:
        print "[FAIL][HTTP] %s - %s "%(hook['artist'],hook['album'])
        db.itunes_store_not_found.insert(hook)
    i+=1;
    pbar.update(i)
pbar.finish()
