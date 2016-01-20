import scrapy

class ArtistItem(scrapy.Item):
    name = scrapy.Field()
    stag = scrapy.Field()
    url = scrapy.Field()
    img = scrapy.Field()
    rank = scrapy.Field()

