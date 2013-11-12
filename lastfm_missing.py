import requests
import json
import traceback


#arts = content.split('\n')
from pymongo import MongoClient
#connection = MongoClient('db.image-quick.com')
#connection = MongoClient('10.0.0.10:27017')
db_ip = 'localhost'
#db_ip = 'localhost'
#db_ip = 'db.image-quick.com'
connection = MongoClient(db_ip)
db = connection.album_art
songs = open('missing.txt', 'r')
def clean(song):
    song.replace('\n','')
    song = song.split('(')[0]
    query = {'artist': song.split('_')[0], 'album': song.split('_')[1]}
    return query
with open('missing.txt') as f:
    content = f.readlines()
songs = [clean(x) for x in content]   



for hook in songs:
    try:
        api = requests.get(
            'http://ws.audioscrobbler.com/2.0/?method=track.search&track=%s&artist=%s&api_key=c85e43eeb52ffc10176d342353882057&format=json' %
            (hook['album'], hook['artist']))
        print "[FETCH] %s"%(hook['album'])
        results = api.json()['results']['trackmatches']
        if results:
            if type(results['track']==dict)
                print "[FOUND] %s"%(hook['album'])
                db.missing_titles_found.insert(results['track'])
            else:
                for track in results['track']:
                    if (hook['artist'].split(' ')[0]).lower() in track['artist'].lower() and flag==0:
                        db.lastfm_titles_found.insert(track)
                        print "[FOUND] %s"%(hook['title'])
                        flag =1
                        break
                if flag==0:
                    print "[FAIL] %s"%(hook['title'])
                    db.lastfm_titles_not_found.insert(hook)

        else:
            print "[FAIL] %s"%(hook['album'])
            db.missing_titles_not_found.insert(hook)
    except:
        print traceback.format_exc()
        print "[FAIL][HTTP] %s "%(hook['album'])
        db.missing_titles_not_found.insert(hook)
