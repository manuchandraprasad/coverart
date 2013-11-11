from config import * 
mbid = MongoClient().mbid
from pprint import pprint
format = {}
for h in db.new_hooks.find({'album_art': "http://image-quick.com/default-album-artwork.png"}):
	if format[h['format']]:
		format[h['format']]+=1
	else:
		format[h['format']] = 1
pprint(format)