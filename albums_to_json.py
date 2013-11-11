import csv
try:
    f = open('artist_titles_albums.csv','rt')
    fieldnames = ('artist', 'title', 'album')
    reader = csv.DictReader(f, fieldnames=fieldnames)
    for row in reader:
            print row

finally:
    f.close()