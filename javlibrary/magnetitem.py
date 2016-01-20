import scrapy

class MagnetItem(scrapy.Item):
    tag = scrapy.Field()
    magnet = scrapy.Field()
