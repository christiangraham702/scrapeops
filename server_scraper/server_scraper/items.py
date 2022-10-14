# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


class ListCraigItem(scrapy.Item):
    title = scrapy.Field(
        output_processor=MapCompose(lambda x: x[0])
    )
    price = scrapy.Field(
        output_processor=MapCompose(lambda x: x[0])
    )
    date = scrapy.Field(
        output_processor=MapCompose(lambda x: x[0])
    )
    region = scrapy.Field(
        output_processor=MapCompose(lambda x: x[0])
    )
    link = scrapy.Field(
        output_processor=MapCompose(lambda x: x[0])
    )
    pid = scrapy.Field(
        output_processor=MapCompose(lambda x: x[0])
    )
    zip_code = scrapy.Field(
        output_processor=MapCompose(lambda x: x[0])
    )
    dist_from_zip = scrapy.Field(
        output_processor=MapCompose(lambda x: x[0])
    )
    num_items = scrapy.Field(
        output_processor=MapCompose(lambda x: x[0])
    )


class ListCraigStateItem(scrapy.Item):
    title = scrapy.Field(output_processor=MapCompose(lambda x: x[0]))
    price = scrapy.Field(output_processor=MapCompose(lambda x: x[0]))
    date = scrapy.Field(output_processor=MapCompose(lambda x: x[0]))
    region = scrapy.Field(output_processor=MapCompose(lambda x: x[0]))
    link = scrapy.Field(output_processor=MapCompose(lambda x: x[0]))
    pid = scrapy.Field(output_processor=MapCompose(lambda x: x[0]))
    zip_code = scrapy.Field(output_processor=MapCompose(lambda x: x[0]))
    dist_from_zip = scrapy.Field(output_processor=MapCompose(lambda x: x[0]))
    num_items = scrapy.Field(output_processor=MapCompose(lambda x: x[0]))
    state = scrapy.Field(output_processor=MapCompose(lambda x: x[0]))
