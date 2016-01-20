import scrapy

class FilmItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    cover = scrapy.Field()
    date = scrapy.Field()
    length = scrapy.Field()
    director = scrapy.Field()
    maker = scrapy.Field()
    producer = scrapy.Field()
    score = scrapy.Field()
    category = scrapy.Field()
    cast = scrapy.Field()
    url = scrapy.Field()
