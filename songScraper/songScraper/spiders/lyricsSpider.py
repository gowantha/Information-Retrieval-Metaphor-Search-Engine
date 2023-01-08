import scrapy
import json

class LyricsSpider(scrapy.Spider):
    name = "lyricsww"



    start_urls = []
    with open("songs.json") as f:
        data = json.load(f)
    for x in data:
        start_urls.append(x.get('link'))

    def parse(self, response):
        songName = response.url.split('/')[-2]
        fileName = songName
        filePath = 'fullSongs/'+fileName

        with open(filePath, 'wb' ) as file1:
            file1.write(response.body)