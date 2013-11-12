from config import db
import json
import requests
from pprint import pprint
from progressbar import ProgressBar,Bar,Percentage
from pymongo import MongoClient
import traceback
#connection = MongoClient('db.image-quick.com')
#connection = MongoClient('10.0.0.10:27017')
db_ip = 'localhost'
#db_ip = 'localhost'
#db_ip = 'db.image-quick.com'
connection = MongoClient(db_ip)
db = connection.album_art
pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=db.lastfm_not_found.find().count()).start()
i=0

for hook in db.lastfm_not_found.find():
    try:
        del hook['_id']
        link = 'http://ws.audioscrobbler.com/2.0/?method=track.search&track=%s&api_key=c85e43eeb52ffc10176d342353882057&format=json' % (
            hook['title'])
        print "[FETCH] %s"%(hook['title'])
        last_fm_api = requests.get(link)
        results = last_fm_api.json()['results']['trackmatches']
        if results:
            for track in results['track']:
                if (hook['artist'].split(' ')[0]).lower() in track['artist'].lower():
                    db.lastfm_titles_found.insert(results['track'])
                    print "[FOUND] %s"%(hook['title'])
                    break
        else:
            print "[FAIL] %s"%(hook['title'])
            db.lastfm_titles_not_found.insert(hook)
    except:
        print traceback.format_exc()
        print "[FAIL][HTTP] %s "%(hook['title'])
        db.lastfm_titles_not_found.insert(hook)
    i+=1;
    pbar.update(i)
pbar.finish()
