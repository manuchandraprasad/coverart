from config import * 
mbid = MongoClient().mbid
from pprint import pprint

for h in db.new_hooks.find({'album_art': "http://image-quick.com/default-album-artwork.png"}):
	album = h['song'].split('(')[0]
	m = mbid.musicbrainz.find_one({'album':album,'artist':h['artist']})
	#print m
	if m:
		h['album_art'] = m['artwork']['images'][0]['thumbnails']['small']
		db.new_hooks.save(h)