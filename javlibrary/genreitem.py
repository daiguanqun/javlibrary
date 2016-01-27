import scrapy

class GenreItem(scrapy.Item):
    url = scrapy.Field();
    name = scrapy.Field()

