from config import *
import json,requests
from pprint import pprint

songs = open('missing.txt','r')
with open('missing.txt') as f:
    content = f.readlines()

#arts = content.split('\n')
def clean(song):
	song.replace('\n','')
	song = song.split('(')[0]
	query = {'artist':song.split('_')[0],'album':song.split('_')[1]}
	return query

arts = [clean(x) for x in content]
pprint(arts)
