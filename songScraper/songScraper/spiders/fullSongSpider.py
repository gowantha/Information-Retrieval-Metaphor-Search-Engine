import scrapy
import json

class LyricsSpider(scrapy.Spider):
    name = "lyrics"

    start_urls = []
    with open("songs3.json") as f:
        data = json.load(f)
    for x in data:
        start_urls.append(x.get('link'))

    def getLyrics(self, rawTexts):
        rawLyrics = []
        for rawText in rawTexts:
            rawLyrics = rawLyrics + rawText.split('\n')

        lyricsLines = []
        for line in rawLyrics:
            isValid = True
            if len(line) == 0:
                isValid = False
            for letterInd in range(len(line)):
                if (ord(line[letterInd - 1]) in range(65, 91) or ord(line[letterInd - 1]) in range(97, 123)):
                    isValid = False
                    break
            if (isValid):
                lyricsLines.append(line.strip())

        refinedLyrics = [value for value in lyricsLines if (value != "" and "|" not in value)]
        lyrics = ""
        for lineInd in range(len(refinedLyrics)):
            lyrics += refinedLyrics[lineInd]
            if lineInd != len(refinedLyrics) - 1:
                lyrics += "\n"
        return lyrics

    def getArtists(self, rawArtistsList):
        return list(set(rawArtistsList))

    def getLyricists(self, rawLyricistsList, backupList):
        lyricists = list(set(rawLyricistsList))
        if not lyricists and backupList:
            possibleLyricists1 = [value for value in backupList if ('Lyrics' in value)]
            if possibleLyricists1:
                possibleLyricists = possibleLyricists1[0].split(":")
                for possibleLyricist in possibleLyricists:
                    lyricists.append(possibleLyricist.strip())
        return list(set(lyricists))

    def getMusicComposers(self, rawMusicComposersList, backupList):
        musicComposers = list(set(rawMusicComposersList))
        if not musicComposers:
            possibleMusicComposers1 = [value for value in backupList if ('Music' in value)]
            if possibleMusicComposers1:
                possibleMusicComposers = possibleMusicComposers1[0].split(":")
                for possibleMusicComposer in possibleMusicComposers:
                    musicComposers.append(possibleMusicComposer.strip())
        return list(set(musicComposers))

    def getGenres(self, rawGenresList):
        return list(set(rawGenresList))




    def parse(self, response):
        # songName = response.url.split('/')[-2]
        # fileName = songName
        # filePath = 'fullSongs/'+fileName
        #
        # with open(filePath, 'wb' ) as file1:
        #     file1.write(response.body)
        songName = response.css("h1.entry-title::text").get()
        artists = self.getArtists(response.css("span.entry-categories a::text").getall())
        lyricists = self.getLyricists(response.css("span.lyrics a::text").getall(), response.css("li::text").getall())
        musicComposers = self.getMusicComposers(response.css("span.music a::text").getall(), response.css("li::text").getall())
        genres = self.getGenres(response.css("span.entry-tags a::text").getall())
        lyrics = self.getLyrics(response.css("pre::text").getall())
        n = None

        yield {
            'songName': songName,
            'artists' : artists,
            'lyricists' : lyricists,
            'musicComposers' : musicComposers,
            'genres' : genres,
            'lyrics' : lyrics,
            'metaphors' : [{
                'metaphor' : None,
                'interpretation' : None
            }]
        }