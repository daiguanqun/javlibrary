import scrapy
import urlparse
from javlibrary.magnetitem import MagnetItem
from javlibrary.db import db
from javlibrary.db.film import Film

class MagnetSpider(scrapy.Spider):
    name = 'Magnet'
    allowed_domian = ['btdigg.org']
    base_url = 'http://btdigg.org/search?info_hash=&q='
    session = db.getsession()
    start_urls = [ base_url + result.tag for result in session.query(Film.tag) ][0:1]
    session.close()

    def parse(self, response):
        tag = urlparse.parse_qs(urlparse.urlparse(response.url).query)['q']
        for href in response.xpath('//td[@class="ttth"]').css('a::attr(href)'):
            magnet = MagnetItem()
            magnet['tag'] = tag
            magnet['magnet'] = href.extract().encode('utf-8')
            yield magnet
