import json
import traceback
from pymongo import MongoClient
import requests
from pprint import pprint
db_ip = 'localhost'
connection = MongoClient(db_ip)
db = connection.imagequick_dev
al_db = connection.album_art
def clean(hook):
    del hook['_id']
    hook['artist'] = hook['hook'].split('_')[0]
    hook['song'] = (hook['hook'].split('(')[0]).split('_')[1]
    return hook

songs = []
for hook in db.hooks.find():
    songs.append(clean(hook))
 

for hook in songs:
    try:
        api = requests.get(
            'http://ws.audioscrobbler.com/2.0/?method=track.search&track=%s&artist=%s&api_key=c85e43eeb52ffc10176d342353882057&format=json' %
            (hook['song'], hook['artist']))
        print "[FETCH] %s"%(hook['song'])
        results = api.json()['results']['trackmatches']
        if results:
            if type(results['track'])==dict:
                print "[FOUND] %s"%(hook['song'])
                if 'image' in results['track'].keys():
                    hook['album_art'] = results['track']['image'][1]['text']
                    db.h_new.insert(hook)
                    #http://image-quick.com/default-album-artwork.png
                else:
                    hook['album_art'] = "http://image-quick.com/default-album-artwork.png"
                    print "[FAIL][NO IMAGE] %s"%(hook['song' ])
                    al_db.missing_titles_not_found.insert(hook)
            else:
                flag=0
                for track in results['track']:
                    if (hook['artist'].split(' ')[0]).lower() in track['artist'].lower() and flag==0:
                        if 'image' in track.keys():
                            print "[FOUND] %s"%(hook['song'])
                            hook['album_art'] = track['image'][1]['text']
                            db.h_new.insert(hook)
                            flag=1
                            break
                if flag==0:
                    print "[FAIL] %s"%(hook['song' ])
                    hook['album_art'] = "http://image-quick.com/default-album-artwork.png"
                    db.h_new.insert(hook)
                    hook['album_art'] 
                    al_db.missing_titles_not_found.insert(hook)

        else:
            print "[FAIL] %s"%(hook['song'])
            hook['album_art'] = "http://image-quick.com/default-album-artwork.png"
            db.h_new.insert(hook)
            del hook['album_art'] 
            al_db.missing_titles_not_found.insert(hook)
    except:
        print traceback.format_exc()
        print "[FAIL][HTTP] %s "%(hook['song'])
        hook['album_art'] = "http://image-quick.com/default-album-artwork.png"
        db.h_new.insert(hook)
        hook['album_art'] 
        al_db.missing_titles_not_found.insert(hook)
