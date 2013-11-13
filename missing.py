from config import * 
from pprint import pprint
for h in db.h_new.find({'album_art': "http://image-quick.com/default-album-artwork.png"}):
	h['album_art'] = 'https://s3.amazonaws.com/album_arts/'+h['hook']+'.jpg'
	db.h_new.save(h)