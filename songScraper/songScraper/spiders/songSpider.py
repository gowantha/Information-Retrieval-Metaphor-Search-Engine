import scrapy

class SongSpider(scrapy.Spider):
    name = 'songs'

    # start_urls = ['https://www.sinhalasongbook.com/category/t-m-jayarathna/',
    #               'https://www.sinhalasongbook.com/category/nanda-malani/',
    #               'https://www.sinhalasongbook.com/category/sunil-edirisinghe/',
    #               'https://www.sinhalasongbook.com/category/amaradewa/',
    #               'https://www.sinhalasongbook.com/category/gunadasa-kapuge/']
    start_urls = ['https://www.sinhalasongbook.com/category/gunadasa-kapuge/page/2/',
                  'https://www.sinhalasongbook.com/category/nanda-malani/page/2/',
                  'https://www.sinhalasongbook.com/category/nanda-malani/page/3/',
                  'https://www.sinhalasongbook.com/category/amaradewa/page/2/',
                  'https://www.sinhalasongbook.com/category/amaradewa/page/3/'
                  ]

    def parse(self, response):
        # artist = response.url.split('/')[-2]
        # fileName = 'songsBy%s.html' % artist
        # with open(fileName, 'wb') as f:
        #     f.write(response.body)

        # for song in response.css('main.content  div.articles article::attr(aria-label)').getall():
        songs = response.css('main.content  div.articles article')
        songLinks = []
        for song in response.css('main.content  div.articles article'):
            songLinks.append(song.css('a.entry-title-link::attr(href)').get())
            yield {
                'song': song.css('a::text').get(),
                'artist': response.css('h1.archive-title::text').get(),
                'link': song.css('a.entry-title-link::attr(href)').get()
            }