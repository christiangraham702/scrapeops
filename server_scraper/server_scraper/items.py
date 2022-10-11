# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ListCraigItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    date = scrapy.Field()
    region = scrapy.Field()
    link = scrapy.Field()
    pid = scrapy.Field()
    zip_code = scrapy.Field()
    dist_from_zip = scrapy.Field()
