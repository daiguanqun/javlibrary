import scrapy
import string
import logging
from javlibrary.artistitem import ArtistItem
from javlibrary.filmitem import FilmItem
from javlibrary.genreitem import GenreItem
from javlibrary.db import db
from javlibrary.db.artist import Artist

class ArtistSpider(scrapy.Spider):
    name = 'Artist'
    allowed_domian = ['javlibrary.com']
    base_url = 'http://www.javlibrary.com/cn/star_list.php'
    start_urls = [ base_url + '?prefix=' + c for c in string.ascii_uppercase]
    def parse(self, response):
        for href in response.xpath('//a[@class="page next"]').css('a::attr("href")'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse)
        for artist in response.xpath('//div[@class="searchitem"]'):
            artistItem = Artist()
            artistItem['name'] = artist.css('a').re('<a?.*>(.*)</a>')[0].encode('utf-8')
            artistItem['stag'] = artist.css('div::attr("id")').extract()[0].encode('utf-8')
            artistItem['url'] = artist.css('a::attr("href")').extract()[0].encode('utf-8')
            yield artistItem

class TopArtistSpider(scrapy.Spider):
    name = 'TopArtist'
    allowed_domian = ['javlibrary.com']
    start_urls = [
            'http://www.javlibrary.com/cn/star_mostfav.php'
            ]

    def parse(self, response):
        for artist in response.xpath('//div[@class="searchitem"]'):
            artistItem = ArtistItem()
            artistItem['name'] = artist.css('img::attr("title")').extract()[0].encode('utf-8')
            artistItem['stag'] = artist.css('div::attr("id")').extract()[0].encode('utf-8')
            artistItem['url'] = artist.css('a::attr("href")').extract()[0].encode('utf-8')
            artistItem['img'] = artist.css('img::attr("src")').extract()[0].encode('utf-8')
            artistItem['rank'] = int(artist.re('#(\d+) ')[0].encode('utf-8'))
            yield artistItem

class GenreSpider(scrapy.Spider):
    name = 'Genre'
    allowed_domian = ['javlibrary.com']
    start_urls = [
            'http://www.javlibrary.com/cn/genres.php'
            ]

    def parse(self, response):
        for genre in response.xpath('//div[@class="genreitem"]'):
            genreItem = GenreItem()
            genreItem['name'] = genre.xpath('a/text()').extract()[0].encode('utf-8')
            genreItem['url'] = genre.css('a::attr("href")').extract()[0].encode('utf-8')
            yield genreItem


class FilmSpider(scrapy.Spider):
    name = 'Film'
    allowed_domian = ['javlibrary.com']
    base_url = 'http://www.javlibrary.com/cn/'
    session = db.getsession()
    start_urls = [ base_url + result.url for result in session.query(Artist.url) ]
    session.close()

    def parse(self, response):
        for href in response.xpath('//div[@class="video"]').css('a::attr(href)'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_one_film)
        for href in response.xpath('//a[@class="page next"]').css('a::attr("href")'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse)

    def parse_one_film(self, response):
        film = FilmItem()
        film['id'] = self.getstring(response.xpath('//div[@id="video_id"]/table/tr/td[@class="text"]/text()'))
        film['name'] = self.getstring(response.xpath('//h3[@class="post-title text"]/a/text()'))
        film['cover'] = self.getstring(response.xpath('//img[@id="video_jacket_img"]').css('img::attr(src)'))
        film['date'] = self.getstring(response.xpath('//div[@id="video_date"]/table/tr/td[@class="text"]/text()'))
        film['length'] = int(self.getstring(response.xpath('//div[@id="video_length"]/table/tr/td/span/text()')))
        film['director'] = self.getstring(response.xpath('//div[@id="video_director"]/table/tr/td/span/a/text()'))
        film['maker'] = self.getstring(response.xpath('//div[@id="video_maker"]/table/tr/td/span/a/text()'))
        film['producer'] = self.getstring(response.xpath('//div[@id="video_label"]/table/tr/td/span/a/text()'))
        scorestring = response.xpath('//span[@class="score"]').re("\((.*)\)")
        if len(scorestring) == 0:
            film['score'] = float(0)
        else:
            film['score'] =  float(scorestring[0].encode('utf-8'))
        film['category'] = [ gen.extract().encode('utf-8') for gen in response.xpath('//span[@class="genre"]/a/text()') ]
        film['cast'] = [star.extract().encode('utf-8')for star in response.xpath('//span[@class="star"]/a').css('a::attr(href)')]
        film['url'] = response.url
        yield film

    def getstring(self, selector):
        if len(selector) == 0:
            return None
        else:
            return selector.extract()[0].encode('utf-8')
