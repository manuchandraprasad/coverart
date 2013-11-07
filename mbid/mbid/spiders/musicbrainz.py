from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
import json
from pprint import pprint
from mbid.items import MbidItem

class MusicbrainzSpider(BaseSpider):
    name = "musicbrainz"
    #allowed_domains = ["http://musicbrainz.org/"]
    start_urls = (
        'http://www.http://musicbrainz.org//',
    )

    def start_requests(self):
        songs = open('missing.txt', 'r')
        with open('missing.txt') as f:
            content = f.readlines()

        #arts = content.split('\n')
        def clean(song):
            song.replace('\n', '')
            song = song.split('(')[0]
            query = {'artist': song.split('_')[
                     0], 'album': song.split('_')[1]}
            return query

        songs = [clean(x) for x in content]
        requests = []
        for song in songs:
            requests.append(
                Request(
                    "http://musicbrainz.org/ws/2/release-group?query=%s %s" %
                    (song['artist'], song['album']), callback=self.parse,meta=song))
        return requests


    def parse(self, response):
    	sel = Selector(response)
    	sel.remove_namespaces()
        mbid = sel.xpath("//release-group[1]/@id").extract()
        if mbid:
            yield Request("http://coverartarchive.org/release-group/"+mbid[0],callback=self.parse_album,meta=response.meta)

    def parse_album(self,response):
        sel = Selector(response)
        data = json.loads(response.body)
        item = MbidItem(
                album = response.meta['album'],
                artist = response.meta['artist'],
                artwork = data
            )
        yield item


    